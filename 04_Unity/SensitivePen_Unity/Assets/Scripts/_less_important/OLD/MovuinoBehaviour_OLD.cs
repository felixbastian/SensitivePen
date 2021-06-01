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
    public class MovuinoBehaviour_OLD : MonoBehaviour
    {

        public OSC oscManager;
        private string addressSensorData;

        private MovuinoBehaviour movuino;
        [SerializeField]
        private string movuinoAdress;

        private void Awake()
        {
            //movuino = new MovuinoSensor(movuinoAdress);
            addressSensorData = movuino.movuinoAdress + movuino.OSCmovuinoSensorData.OSCAddress;
        }
        void Start()
        {
            oscManager.SetAddressHandler(movuino.movuinoAdress, movuino.OSCmovuinoSensorData.ToOSCDataHandler);
            //oscManager.SetAllMessageHandler(OSCDataHandler.DebugAllMessage);
        }


        private void FixedUpdate()
        {
            movuino.UpdateMovuinoData();
            //this.gameObject.transform.Rotate(movuino.InstantGyroscope * Time.fixedDeltaTime * (float)(360/(2*3.14)));
            movuino.InitMovTransform();
            this.gameObject.transform.Translate(new Vector3(movuino.angleMagOrientation.y * (float)0.001, -movuino.angleMagOrientation.x * (float)0.001, 0) );
            Debug.Log(movuino.angleMagOrientation);
        }

        void GetGyroriantation(OSCMovuinoSensorData movuino)
        {
            this.gameObject.transform.Rotate(movuino.gyroscope * Time.fixedDeltaTime * (float)(360.0 / (2 * 3.14)));
        }
        void MoveObj(OSCMovuinoSensorData movuino)
        {
            this.gameObject.transform.Translate(movuino.accelerometer * Time.fixedDeltaTime);
        }

        void OrientObj(OSCMovuinoSensorData movuino)
        {
            //this.gameObject.transform.localEulerAngles = Angle;
        }


    }

}