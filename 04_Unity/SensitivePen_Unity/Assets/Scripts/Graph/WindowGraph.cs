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
        [SerializeField] private MovuinoBehaviour movuinoBehaviour;

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
            //Data of differents curve
            curveList[0].valueList.Add(movuinoBehaviour.angleAccelOrientationSmooth.x); //movuinoBehaviour.MovingMean(movuinoBehaviour.angleAccelOrientation.x, ref movuinoBehaviour.listMeanX)
            curveList[1].valueList.Add(movuinoBehaviour.angleAccelOrientationSmooth.y);
            curveList[2].valueList.Add(movuinoBehaviour.angleAccelOrientationSmooth.z);

            angleX.text = "Angle X : " + (int)movuinoBehaviour.angleAccelOrientationSmooth.x;
            angleY.text = "Angle Y : " + (int)movuinoBehaviour.angleAccelOrientationSmooth.y;
            angleZ.text = "Angle Z : " + (int)movuinoBehaviour.angleAccelOrientationSmooth.z;

            for (int k =0; k<nbCurve; k++)
            {
                curveList[k].RefreshCurve();
            }
        }

    }



}