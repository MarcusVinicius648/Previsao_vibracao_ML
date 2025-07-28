import sqlite3
import os
from math import sqrt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class VibrationBackend:
    def __init__(self, db_name='vibration_data.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vibration_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    distancia REAL NOT NULL,
                    carga_espera REAL NOT NULL,
                    vibracao REAL NOT NULL  ,
                    litologia TEXT NOT NULL,
                    k REAL,
                    alpha REAL,                           
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            print("✅ Database initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            return False
    
    def save_data(self, distance, charge, vibration, lithology):
        """Save vibration data to the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO vibration_data (distancia, carga_espera, vibracao, litologia)
                VALUES (?, ?, ?, ?)
            ''', (distance, charge, vibration, lithology))
            conn.commit()
            conn.close()
            print(f"✅ Data saved: D={distance}m, C={charge}kg, V={vibration}mm/s, L={lithology}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    def get_all_data(self):
        """Retrieve all data from the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, distancia, carga_espera, vibracao, litologia 
                FROM vibration_data 
                ORDER BY id DESC
            ''')
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            print(f"❌ Error retrieving data: {e}")
            return []
    
    def get_lithologies(self):
        """Get unique lithologies from the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT litologia FROM vibration_data ORDER BY litologia")
            lithologies = [row[0] for row in cursor.fetchall()]
            conn.close()
            return lithologies
        except Exception as e:
            print(f"❌ Error getting lithologies: {e}")
            return []
    
    def get_data_by_lithology(self, lithology):
        """Get all data for a specific lithology"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT distancia, carga_espera, vibracao 
                FROM vibration_data 
                WHERE litologia = ?
            ''', (lithology,))
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            print(f"❌ Error getting data for lithology {lithology}: {e}")
            return []
    
    def calculate_k_factor(self):
        """Calculate K-factor for vibration prediction"""
        try:
            #calcular as constantes
            conn = sqlite3.connect(self.db_name)
            query = "SELECT distancia, carga_espera, vibracao, litologia FROM vibration_data"
            df = pd.read_sql_query(query,conn)
            
            for litologia, grupo in df.groupby('litologia'):
                
                grupo['X'] = np.log10(grupo['distancia'] / np.sqrt(grupo['carga_espera']))
                grupo['Y'] = np.log10(grupo['vibracao'])
                
                X = grupo[['X']]
                y = grupo['Y']
                
                modelo = LinearRegression().fit(X,y)

                m = -modelo.coef_[0]
                log_k = modelo.intercept_
                k = 10 ** log_k
                
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE vibration_data
                    SET k = ?, alpha = ?
                    WHERE litologia = ?
                """, (k, m, litologia))

                conn.commit()

            conn.close()

        except Exception as e:
            print(f"❌ Error calculating K-factor: {e}")
            return None
    
    def predict_vibration(self, distance, charge, lithology):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT k, alpha FROM vibration_data WHERE litologia = ? LIMIT 1", (lithology,))
            resultado = cursor.fetchone()
            K, alpha = resultado
            
            # Predict vibration using the K-factor method
            # V = K / (D/√Q)^B
            scaled_distance = float(distance) / sqrt(float(charge))
            predicted_vibration = K / (scaled_distance ** alpha)
            
            print(f"📊 Prediction details:")
            print(f"   - Lithology: {lithology}")
            print(f"   - Predicted vibration: {predicted_vibration:.2f} mm/s")

            conn.close()
            
            return f"{predicted_vibration:.2f} mm/s"
            
            
        except Exception as e:
            print(f"❌ Error in vibration prediction: {e}")
            return "Erro na previsão"
    
