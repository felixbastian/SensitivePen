using System.Collections;
using System.Collections.Generic;
using Device;
using UnityEngine;

namespace Movuino
{
    /// <summary>
    /// Class that manage the movuino object in the scene
    /// </summary>
    /// <remarks>Handle OSC conncetion too</remarks>
    public class MovuinoBehaviour : MonoBehaviour
	{
        public OSC oscManager;

        [SerializeField]
        private string _movuinoAdress;

        private string _addressSensorData;

        public OSCMovuinoSensorData OSCmovuinoSensorData; //9axes data

        public string movuinoAdress { get { return _movuinoAdress; } }
        public Vector3 instantAcceleration { get { return OSCmovuinoSensorData.accelerometer; } }
        public Vector3 instantGyroscope { get { return OSCmovuinoSensorData.gyroscope; } }
        public Vector3 instantMagnetometer { get { return OSCmovuinoSensorData.magnetometer; } }

        public Vector3 acceleration { get { return _accel; } }
        public Vector3 gyroscope { get { return (_gyr-_initGyr)*(float)(360/(2*3.14)); } }
        public Vector3 magnetometer { get { return _mag; } }

        public Vector3 deltaAccel { get { return _accel - _prevAccel;  } }
        public Vector3 deltaGyr { get { return _gyr - _prevGyr;  } }
        public Vector3 deltaMag { get { return _mag - _prevMag;  } }

        public Vector3 angleOrientation {  get { return GetAngleMag(); } }
        public Vector3 angleGyrOrientation {  get { return GetAngleGyrEulerIntegratino(); } }


        public Vector3 _accel;
        Vector3 _gyr;
        Vector3 _mag;

        Vector3 _prevAccel;
        Vector3 _prevGyr;
        Vector3 _prevMag;

        Vector3 _initAngle;
        Vector3 _initGyr;
        Vector3 _initAccel;
        Vector3 _initMag;
        Vector3 _angleMagMethod;
        Vector3 _angleGyrMethod;

        private void Awake()
        {
            Init();
            _addressSensorData = movuinoAdress + OSCmovuinoSensorData.OSCAddress;
        }
        void Start()
        {
            oscManager.SetAddressHandler(movuinoAdress, OSCmovuinoSensorData.ToOSCDataHandler);
            //oscManager.SetAllMessageHandler(OSCDataHandler.DebugAllMessage);
        }


        private void FixedUpdate()
        {
            UpdateMovuinoData();
            InitMovTransform();
            
        }


        Vector3 GetAngleGyrEulerIntegratino()
        {
            Vector3 angle = new Vector3();

            angle.x = _angleGyrMethod.x + _gyr.x * Time.deltaTime;
            angle.x = _angleGyrMethod.y + _gyr.y * Time.deltaTime;
            angle.x = _angleGyrMethod.z + _gyr.z * Time.deltaTime;
            return angle;
        }


        public void Init()
		{
            _prevAccel = new Vector3(0, 0, 0);
            _prevGyr = new Vector3(0, 0, 0);
            _prevMag = new Vector3(0, 0, 0);

            _accel = new Vector3(0, 0, 0);
            _gyr = new Vector3(0, 0, 0);
            _mag = new Vector3(0, 0, 0);

            _angleGyrMethod = new Vector3(0, 0, 0);
            _angleMagMethod = new Vector3(0, 0, 0);
            _initAngle = new Vector3(0, 0, 0);
            _initGyr = new Vector3(0, 0, 0);
            _initAccel = new Vector3(0, 0, 0);
            _initMag = new Vector3(0, 0, 0);
            OSCmovuinoSensorData = OSCDataHandler.CreateOSCDataHandler<OSCMovuinoSensorData>();
        }


        Vector3 GetAngleMag()
        {
            _angleMagMethod = OSCmovuinoSensorData.magnetometer - _initAngle;
            return _angleMagMethod;
        }

        public void InitMovTransform()
        {

            if (Input.GetKeyDown(KeyCode.I))
            {
                _initAngle = OSCmovuinoSensorData.magnetometer;
            }
            if (Input.GetKeyDown(KeyCode.Y))
            {
                _initGyr = OSCmovuinoSensorData.gyroscope;
                _initMag = OSCmovuinoSensorData.magnetometer;
                _initAccel = OSCmovuinoSensorData.accelerometer;
            }

        }

        public void UpdateMovuinoData()
        {
            _prevAccel = _accel;
            _prevGyr = _gyr;
            _prevMag = _mag;

            _angleGyrMethod = GetAngleGyrEulerIntegratino();
            _angleMagMethod = GetAngleMag();

            _accel = instantAcceleration;
            _gyr = instantGyroscope;
            _mag = instantMagnetometer;

        }

    }

}