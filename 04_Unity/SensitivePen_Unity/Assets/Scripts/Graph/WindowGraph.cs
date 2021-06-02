using System;
using System.Collections;
using System.Collections.Generic;
using Movuino;
using UnityEngine;
using UnityEngine.UI;


namespace Graph
{
    /// <summary>
    /// Class that manages the graph representation
    /// </summary>
    public class WindowGraph : MonoBehaviour
    {
        //---- Window part -----
        [SerializeField] private Sprite circleSprite;
        [SerializeField] private RectTransform graphContainer;
        [SerializeField] private Curve curvePrefab;
        [SerializeField] private int _yMax;
        [SerializeField] private int nbDot;
        private List<Curve> curveList;
        private int nbCurve;

        private GameObject rawDataText;

        //usefull bc movuino
        private Text angleX;
        private Text angleY;
        private Text angleZ;

        //--------- Movuino part -----
        [SerializeField] private SensitivePenBehaviour_visu sensitivePen;

        //test
        private List<float> liste;
        private int i = 0;

        private void Awake()
        {
            //CreateCircle(new Vector2(200, 200));
            //liste = new List<float>();
            curveList = new List<Curve>();
            nbCurve = 3;

            //Instantiation and initialisation of curves
            for (int k = 0; k < nbCurve; k++)
            {
                GameObject go = Instantiate(curvePrefab.gameObject, graphContainer);
                go.GetComponent<Curve>().Init(circleSprite, graphContainer, _yMax, nbDot);
                go.name = go.name + "_" + Curve.index;
                curveList.Add(go.GetComponent<Curve>());
            }

            curveList[0].curveColor = new Color(200, 0, 0);
            curveList[1].curveColor = new Color(0, 200, 0);
            curveList[2].curveColor = new Color(0, 0, 200);

            rawDataText = this.gameObject.transform.Find("RawDataTexte").gameObject;
            angleX = rawDataText.transform.Find("AngleX").GetComponent<Text>();
            angleY = rawDataText.transform.Find("AngleY").GetComponent<Text>();
            angleZ = rawDataText.transform.Find("AngleZ").GetComponent<Text>();
        }
        private void Update()
        {
            float valX=0;
            float valY=0;
            float valZ=0;

            //Data of differents curve
            if (sensitivePen.onlineMode)
            {
                valX = sensitivePen.movuinoBehaviour.angleGyrOrientation.x;
                valY = sensitivePen.movuinoBehaviour.angleGyrOrientation.y;
                valZ = sensitivePen.movuinoBehaviour.angleGyrOrientation.z;
            }
            else if (sensitivePen.offlineMode)
            {
                valX = sensitivePen.movuinoDataSet.acceleration.x;
                valY = sensitivePen.movuinoDataSet.acceleration.y;
                valZ = sensitivePen.movuinoDataSet.acceleration.z;
            }
            else
            {
                valX = 0;
                valY = 0;
                valZ = 0;
            }
           
            curveList[0].valueList.Add(valX); //movuinoBehaviour.MovingMean(movuinoBehaviour.angleAccelOrientation.x, ref movuinoBehaviour.listMeanX)
            curveList[1].valueList.Add(valY);
            curveList[2].valueList.Add(valZ);

            angleX.text = "Angle X : " + (int)valX;
            angleY.text = "Angle Y : " + (int)valY;
            angleZ.text = "Angle Z : " + (int)valZ;

            for (int k =0; k<nbCurve; k++)
            {
                curveList[k].RefreshCurve();
            }
        }

    }



}