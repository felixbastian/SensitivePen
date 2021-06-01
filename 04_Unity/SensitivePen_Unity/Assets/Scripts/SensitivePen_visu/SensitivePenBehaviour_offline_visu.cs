using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Movuino;


public class SensitivePenBehaviour_offline_visu : MonoBehaviour
{
    private MovuinoDataSet movuinoDataSet;

    private string dataPath = "..\\..\\06_Python\\Data\\4polo_2\\record_1_treated.csv";


    private float startTime;
    private int i;
    private bool end;
    public void Awake()
    {
        movuinoDataSet = GetComponent<MovuinoDataSet>();
        movuinoDataSet.Init(dataPath);
        movuinoDataSet.i = 1;

        print("oooook   " + (movuinoDataSet.GetValue("time", 1) - movuinoDataSet.GetValue("time", 0)));
        InvokeRepeating("Rotate", 2f, 0.03f);
    }

    private void Rotate()
    {
        Vector3 deltaTheta = movuinoDataSet.GetVector("posAngY", "posAngX", "posAngZ", movuinoDataSet.i) - movuinoDataSet.GetVector("posAngY", "posAngX", "posAngZ", movuinoDataSet.i - 1);
        this.gameObject.transform.Rotate(deltaTheta);
        print(movuinoDataSet.time);
        movuinoDataSet.i++;


    }
}