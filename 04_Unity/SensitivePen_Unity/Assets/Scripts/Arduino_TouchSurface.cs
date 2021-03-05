using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;
using System.Linq;
using System.Threading;
using UnityEngine.UI;

public class Arduino_TouchSurface : MonoBehaviour
{
	// Thread variables
	public Thread serialThread;
	public SerialPort serial;
	Queue<string> my_queue = new Queue<string> ();
	private int dataCounter = 0;

	public Text consoleText;

	// Sensor grid setup
	public int ROWS = 24;
	public int COLS = 25;

	// Sensor grid variables
	public GameObject datapointPrefab;
	public GameObject[,] pointGrid;

	// Accelerometer variables
	public Vector3 acceleration = Vector3.zero;
	private List<Vector3> accCollection = new List<Vector3> (); // collection storing acceleration data to compute moving mean
	public int nAcc = 5; // max size of accCollection (size of filter)

	void Start ()
	{
		// Initialize point grid as gameobjects
		pointGrid = new GameObject[ROWS, COLS];
		for (int i = 0; i < ROWS; i++) {
			for (int j = 0; j < COLS; j++) {
				float x_ = i * 10;
				float y_ = j * 10;
				pointGrid [i, COLS - j - 1] = GameObject.Instantiate (datapointPrefab, new Vector3 (x_, y_, 0), Quaternion.identity);
			}
		}

		foreach(string str in SerialPort.GetPortNames())
		{
			Debug.Log(str); // print available serial ports
		}
		serial = new SerialPort ("COM4",38400);
		connect ();
		StartCoroutine (printSerialDataRate (1f));
	}

	void connect ()
	{
		Debug.Log ("Connection started");
		try {
			serial.Open ();
			serial.ReadTimeout = 400;
			serial.Handshake = Handshake.None;
			serialThread = new Thread (recDataThread);
			serialThread.Start ();
			Debug.Log ("Port Opened!");
		} catch {
			Debug.Log ("Could not open serial port");
		}
	}

	public void OnApplicationQuit ()
	{
		if (serial != null) {
			if (serial.IsOpen) {
				print ("closing serial port");
				serial.Close ();
			}
			serial = null;
		}
	}

	void recDataThread ()
	{
		if ((serial != null) && (serial.IsOpen)) {
			byte tmp;
			string data = "";
			tmp = (byte)serial.ReadByte ();
			while (tmp != 255) {
				tmp = (byte)serial.ReadByte ();
				if (tmp != 'q') {
					data += ((char)tmp);
				} else {
					my_queue.Enqueue (data);
					data = "";
				}
			}
		}
	}

	void Update ()
	{
		// Get serial data from second thread
		if (my_queue != null && my_queue.Count > 0) {
			int q_length_touch = my_queue.Count;
			for (int i = 0; i < q_length_touch; i++) {
				string rawdatStr_ = my_queue.Dequeue ();
				if (rawdatStr_ != null && rawdatStr_.Length > 1) {
					getSerialData (rawdatStr_);
					consoleText.text = rawdatStr_;
				}
			}
		}

		// Remap and display data points
		for (int i = 0; i < ROWS; i++) {
			// Get row data range
			float minRow_ = 1000.0f;
			float maxRow_ = -1000.0f;
			float sumRow_ = 0.0f;
			for (int j = 0; j < COLS; j++) {
				sumRow_ += pointGrid [i, j].GetComponent<DatapointControl> ().curSRelativeVal;

				if (minRow_ > pointGrid [i, j].GetComponent<DatapointControl> ().curSRelativeVal) {
					minRow_ = pointGrid [i, j].GetComponent<DatapointControl> ().curSRelativeVal;
				}
				if (maxRow_ < pointGrid [i, j].GetComponent<DatapointControl> ().curSRelativeVal) {
					maxRow_ = pointGrid [i, j].GetComponent<DatapointControl> ().curSRelativeVal;
				}
			}

			// Get remap values for the current row and display data point
			for (int j = 0; j < COLS; j++) {
				if (maxRow_ - minRow_ != 0) {
					pointGrid [i, j].GetComponent<DatapointControl> ().curRemapVal = (pointGrid [i, j].GetComponent<DatapointControl> ().curSRelativeVal - minRow_) / (maxRow_ - minRow_);
					pointGrid [i, j].GetComponent<DatapointControl> ().curRemapVal *= sumRow_;
					pointGrid [i, j].GetComponent<DatapointControl> ().curRemapVal /= 1024.0f; // 1024 = max analog range
					pointGrid [i, j].GetComponent<DatapointControl> ().curRemapVal = Mathf.Clamp (pointGrid [i, j].GetComponent<DatapointControl> ().curRemapVal, 0.0f, 1.0f);
				}
			}
		}
	}

	void getSerialData (string serialdata_)
	{		
		serialdata_ = serialdata_.Trim ();

		// First character of the string is an adress
		char adr_ = serialdata_.ToCharArray () [0]; // get address character
		serialdata_ = serialdata_.Split (adr_) [1]; // remove adress from the string to get the message content

		switch (adr_) {
		case 'z':
			// GET COORDINATES
			if (serialdata_ != null) {
				if (serialdata_.Length == 2 + 4 * COLS) {
					//int[] rawdat_ = serialdata_.Split ('x').Select (str => int.Parse (str)).ToArray (); // get 
					int[] rawdat_ = serialdata_.Split ('x').Select (str => int.Parse (str, System.Globalization.NumberStyles.HexNumber)).ToArray ();
					//print (rawdat_.Length);
					//print (COLS+1);
					if (rawdat_.Length == COLS + 1) { // COLS + 1 ROW
						int j = rawdat_ [0];
						for (int k = 1; k < rawdat_.Length; k++) {
							pointGrid [j, k - 1].GetComponent<DatapointControl> ().pushNewRawVal (rawdat_ [k]);
						}
					}
					this.dataCounter++;
				}
			}
			break;

		case 'a':
			// GET ACCELERATION
			if (serialdata_ != null) {
				if (serialdata_.Length == 3*3+2) {
					int[] acc_ = serialdata_.Split ('c').Select (str => int.Parse (str, System.Globalization.NumberStyles.HexNumber)).ToArray ();
					if (acc_.Length == 3) {
						this.accCollection.Add (new Vector3 (acc_ [0], acc_ [1], acc_ [2]));
						while (this.accCollection.Count > this.nAcc) {
							this.accCollection.RemoveAt (0);
						}

						// Compute moving mean filter
						Vector3 smoothAcc_ = Vector3.zero;
						foreach (Vector3 curAcc_ in this.accCollection) {
							smoothAcc_ += curAcc_;
						}
						smoothAcc_ /= (float)this.accCollection.Count; 

						this.acceleration = smoothAcc_;
						this.acceleration /= 10000f; // map acceleration TO CHANGE
						this.dataCounter++;
					}
				} 
			}
			break;

		default:
			break;
		}
	}

	private IEnumerator printSerialDataRate (float waitTime)
	{
		while (true) {
			yield return new WaitForSeconds (waitTime);
			print ("Serial data rate = " + this.dataCounter / waitTime + " data/s");
			this.dataCounter = 0;
		}
	}
}