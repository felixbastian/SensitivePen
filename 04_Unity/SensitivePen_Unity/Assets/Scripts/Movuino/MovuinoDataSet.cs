using System;
using System.IO;
using System.Globalization;
using System.Collections;
using System.Data;
using System.Collections.Generic;
using UnityEngine;

namespace Movuino
{
    /// <summary>
    /// Class That represent a complete file of data of a movuino
    /// </summary>
    public class MovuinoDataSet: MonoBehaviour
    {
        [SerializeField] private string folderPath;
        [SerializeField] private string filename;

        List<object[]> rawData_ = new List<object[]>();
        DataTable _rawData;


        public DataTable rawData
        {
            get { return _rawData; }
        }

        public DataRowCollection table
        {
            get { return _rawData.Rows; }
        }


        public int i;

        #region Properties
        public float time { get { return GetValue("time",i); } }
        public Vector3 acceleration { get { return GetAcceleration(i); } }
        public Vector3 gyroscope { get { return GetGyroscope(i); } }
        public Vector3 magnetometre { get { return GetMagnetometre(i); } }
        #endregion
        #region Methods

        public void Start()
        {
            Init(folderPath + filename);
        }

        public void Init(string dataPath)
        {
            Debug.Log("Reading... " + dataPath);
            //rawData_ = ReadCSV(dataPath);
            _rawData = ConvertCSVtoDataTable(dataPath);
            i = 1;
            Debug.Log(GetValue("posAngX", 25));

        }
        public Vector3 GetVector(string columnX, string columnY, string columnZ, int i)
        {
            float x = GetValue(columnX, i);
            float y = GetValue(columnY, i);
            float z = GetValue(columnZ, i);
            return new Vector3(x, y, z);
        }

        public Vector3 GetAcceleration(int i)
        {
            return GetVector("ax", "ay", "az", i);
        }

        public Vector3 GetGyroscope(int i)
        {
            return GetVector("gx", "gy", "gz", i);
        }

        public Vector3 GetMagnetometre(int i)
        {
            return GetVector("mx", "my", "mz", i);
        }

        /// <summary>
        /// Get a complete column.
        /// </summary>
        /// <param name="columnName"></param>
        /// <returns>List of floats <=> dataTable[columnName].Value</returns>
        public List<float> GetColumn(string columnName)
        {
            List<float> column = new List<float>();

            for (int i = 0; i < _rawData.Columns.Count; i++)
            {
                column.Add(GetValue(columnName, i));
            }

            return column;
        }

        /// <summary>
        /// Get the value of (float)rawData.Rows[index][columnName].
        /// </summary>
        /// <param name="columnName">Column name.</param>
        /// <param name="index">Index of the line.</param>
        /// <returns>Result : (float)_rawData.Rows[index][columnName]</returns>
        public float GetValue(string columnName, int index)
        {
            return (float)_rawData.Rows[index][columnName];
        }

        /// <summary>
        /// Convert a csv file to a datatable.
        /// </summary>
        /// <param name="strFilePath">Path of the csv file.</param>
        /// <returns>Result</returns>
        /// <remarks>Column type is float/System.Single.</remarks>
        public static DataTable ConvertCSVtoDataTable(string strFilePath)
        {
            StreamReader sr = new StreamReader(strFilePath);
            string[] headers = sr.ReadLine().Split(',');
            DataTable dt = new DataTable();

            foreach (string header in headers)
            {
                dt.Columns.Add(header);
                dt.Columns[header].DataType = typeof(float);
            }
            CultureInfo culture = new CultureInfo("en-US");
            while (!sr.EndOfStream)
            {
                string[] rows = sr.ReadLine().Split(',');
                DataRow dr = dt.NewRow();
                for (int i = 0; i < headers.Length; i++)
                {
                    dr[i] = float.Parse(rows[i], culture);
                }
                dt.Rows.Add(dr);
            }
            return dt;
        }

        List<object[]> ReadCSV(string dataPath)
        {

            StreamReader sr = new StreamReader(dataPath);
            char sep = ',';

            string line = sr.ReadLine();

            //We'ra counting the number of column
            int nb_columne = 1;
            foreach (char a in line)
            {
                if (a == sep)
                    nb_columne++;
            }
            List<object[]> data = new List<object[]>(); //All the file
            object[] tData = new object[nb_columne]; //Data for a t time that has a 
            string value = "";
            int i = 0;

            //Header
            foreach (char a in line)
            {
                if (a == ',')
                {
                    tData[i] = value;

                    value = "";
                    i += 1;
                }
                else
                {
                    value += a;
                }

            }
            tData[i] = value;
            data.Add(tData);
            tData = new object[nb_columne];
            value = "";
            line = sr.ReadLine();

            //Data
            while (line != null)
            {
                i = 0;
                //We read all the line
                foreach (char a in line)
                {
                    if (a == ',')
                    {
                        tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                        value = "";
                        i += 1;
                    }
                    else
                    {
                        value += a;
                    }

                }
                tData[i] = float.Parse(value, CultureInfo.InvariantCulture);
                data.Add(tData);
                tData = new object[nb_columne];
                value = "";
                line = sr.ReadLine();
            }
            return data;
        }
        #endregion
    }


}