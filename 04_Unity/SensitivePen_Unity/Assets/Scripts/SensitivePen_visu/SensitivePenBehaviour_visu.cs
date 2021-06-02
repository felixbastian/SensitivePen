using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Movuino;


public class SensitivePenBehaviour_visu : MonoBehaviour
{
    private MovuinoDataSet _movuinoDataSet;
    private MovuinoBehaviour _movuinoBehaviour;

    Vector3 angleAccel;

    bool _onlineMode = false;
    bool _offlineMode = false;

    public bool onlineMode { get { return _onlineMode; } }
    public bool offlineMode { get { return _offlineMode; } }

    public MovuinoDataSet movuinoDataSet { get { return _movuinoDataSet; } }
    public MovuinoBehaviour movuinoBehaviour { get { return _movuinoBehaviour; } }


    private float startTime;
    private int i;
    private bool end;
    public void Start()
    {
        _movuinoDataSet = GetComponent<MovuinoDataSet>();
        _movuinoBehaviour = GetComponent<MovuinoBehaviour>();

        if (_movuinoDataSet.enabled)
        {
            //movuinoDataSet.Init(dataPath);
            _offlineMode = true;
            _onlineMode = false;
            print("Movuino offline");
            InvokeRepeating("Rotate", 2f, 0.03f);
        } 
        else if (_movuinoBehaviour.enabled)
        {
            print("ONline mode");
            _offlineMode = false;
            _onlineMode = true;
        } 
        else if (_movuinoBehaviour.enabled && _movuinoDataSet.enabled)
        {
            print("Impossible to use both modes, please uncheck one");
        }

    }
    public void FixedUpdate()
    {
        if (_onlineMode)
        {
            angleAccel = _movuinoBehaviour.angleGyrOrientation;
            //this.gameObject.transform.Rotate(movuinoBehaviour.gyroscopeRaw * Time.deltaTime);
            this.gameObject.transform.localEulerAngles = new Vector3(angleAccel.x, angleAccel.y, angleAccel.z);
        }


    }

    private void Rotate()
    {
        Vector3 deltaTheta = _movuinoDataSet.GetVector("posAngX", "posAngY", "posAngZ", _movuinoDataSet.i) - _movuinoDataSet.GetVector("posAngX", "posAngY", "posAngZ", _movuinoDataSet.i - 1);
        this.gameObject.transform.Rotate(deltaTheta);
        print(_movuinoDataSet.time);
        _movuinoDataSet.i++;
    }
}