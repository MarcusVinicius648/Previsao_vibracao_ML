import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from backend import VibrationBackend
import pandas as pd

class ModernVibrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Previsão de Vibrações")
        self.geometry("800x600")
        self.configure(bg='#f0f2f5')
        
        # Initialize backend
        self.backend = VibrationBackend()
        
        # Configure style
        self.setup_styles()
        
        # Create container for frames
        container = tk.Frame(self, bg='#f0f2f5')
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Create and add frames to dictionary
        for F in (ModernPredictionPage, ModernDatabasePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Show initial frame
        self.show_frame(ModernPredictionPage)
    
    def setup_styles(self):
        """Setup modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Modern.TButton',
                       background='#4CAF50',
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       padding=(20, 10))
        
        style.configure('Secondary.TButton',
                       background='#2196F3',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8))
        
        style.configure('Danger.TButton',
                       background='#f44336',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8))
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=2,
                       relief='solid',
                       padding=10)
        
        # Configure combobox styles
        style.configure('Modern.TCombobox',
                       fieldbackground='white',
                       borderwidth=2,
                       relief='solid',
                       padding=10)
    
    def show_frame(self, cont):
        """Raise the selected frame to the top"""
        frame = self.frames[cont]
        frame.tkraise()

class ModernPredictionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f2f5')
        self.controller = controller
        
        # Main container with padding
        main_container = tk.Frame(self, bg='#f0f2f5')
        main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='#f0f2f5')
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Title with modern styling
        title_label = tk.Label(header_frame, 
                              text="🔬 Previsão de Vibrações Induzidas", 
                              font=("Arial", 24, "bold"),
                              fg='#2c3e50',
                              bg='#f0f2f5')
        title_label.pack(side="left")
        
        # Modern update database button
        update_btn = tk.Button(header_frame,
                              text="📊 Atualizar BD",
                              font=("Arial", 12, "bold"),
                              bg='#e74c3c',
                              fg='white',
                              relief='flat',
                              padx=20,
                              pady=10,
                              cursor='hand2',
                              command=lambda: controller.show_frame(ModernDatabasePage))
        update_btn.pack(side="right")
        
        # Main content card
        content_card = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        content_card.pack(fill="both", expand=True, pady=0)
        
        # Card header
        card_header = tk.Frame(content_card, bg='#3498db', height=60)
        card_header.pack(fill="x")
        card_header.pack_propagate(False)
        
        card_title = tk.Label(card_header,
                             text="💡 Calcular Previsão de Vibração",
                             font=("Arial", 16, "bold"),
                             fg='white',
                             bg='#3498db')
        card_title.pack(expand=True)
        
        # Input section
        input_section = tk.Frame(content_card, bg='white')
        input_section.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Create input fields with modern styling
        self.create_modern_input_field(input_section, "📏 Distância (m):", 0)
        self.distance_entry = self.last_entry
        
        self.create_modern_input_field(input_section, "⚡ Carga de espera (kg):", 1)
        self.charge_entry = self.last_entry
        
        self.create_modern_combobox_field(input_section, "🗿 Litologia:", 2)
        self.lithology_combobox = self.last_combobox
        self.update_lithology_options()
        
        # Big calculate button
        button_frame = tk.Frame(input_section, bg='white')
        button_frame.grid(row=3, column=0, columnspan=2, pady=30)
        
        calculate_btn = tk.Button(button_frame,
                                 text="🚀 CALCULAR PREVISÃO",
                                 font=("Arial", 16, "bold"),
                                 bg='#27ae60',
                                 fg='white',
                                 relief='flat',
                                 padx=40,
                                 pady=15,
                                 cursor='hand2',
                                 command=self.submit_prediction)
        calculate_btn.pack()
        
        # Result section
        result_frame = tk.LabelFrame(input_section, 
                                   text="📊 Resultado da Previsão",
                                   font=("Arial", 14, "bold"),
                                   fg='#2c3e50',
                                   bg='white',
                                   padx=20,
                                   pady=20)
        result_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=0)
        
        self.result_label = tk.Label(result_frame,
                                   text="Aguardando cálculo...",
                                   font=("Arial", 14),
                                   fg='#7f8c8d',
                                   bg='white')
        self.result_label.pack(pady=10)
        
        # Configure grid weights
        input_section.grid_columnconfigure(1, weight=1)
    
    def create_modern_input_field(self, parent, label_text, row):
        """Create a modern styled input field"""
        label = tk.Label(parent,
                        text=label_text,
                        font=("Arial", 12, "bold"),
                        fg='#2c3e50',
                        bg='white')
        label.grid(row=row, column=0, sticky="w", pady=15, padx=(0, 20))
        
        entry = tk.Entry(parent,
                        font=("Arial", 12),
                        relief='solid',
                        bd=2,
                        bg='#ecf0f1')
        entry.grid(row=row, column=1, sticky="ew", pady=15, ipady=8)
        
        self.last_entry = entry
    
    def create_modern_combobox_field(self, parent, label_text, row):
        """Create a modern styled combobox field"""
        label = tk.Label(parent,
                        text=label_text,
                        font=("Arial", 12, "bold"),
                        fg='#2c3e50',
                        bg='white')
        label.grid(row=row, column=0, sticky="w", pady=15, padx=(0, 20))
        
        combobox = ttk.Combobox(parent,
                               font=("Arial", 12),
                               style='Modern.TCombobox')
        combobox.grid(row=row, column=1, sticky="ew", pady=15, ipady=8)
        
        self.last_combobox = combobox
    
    def update_lithology_options(self):
        """Update the lithology dropdown with options from the database"""
        lithologies = self.controller.backend.get_lithologies()
        self.lithology_combobox['values'] = lithologies
        if lithologies:
            self.lithology_combobox.current(0)
    
    def submit_prediction(self):
        """Handle prediction submission"""
        try:
            distance = self.distance_entry.get()
            charge = self.charge_entry.get()
            lithology = self.lithology_combobox.get()
            
            # Validate inputs
            if not distance or not charge or not lithology:
                messagebox.showerror("❌ Erro", "Por favor, preencha todos os campos")
                return
            
            try:
                distance = float(distance)
                charge = float(charge)
                if distance <= 0 or charge <= 0:
                    messagebox.showerror("❌ Erro", "Distância e carga devem ser valores positivos")
                    return
            except ValueError:
                messagebox.showerror("❌ Erro", "Distância e carga devem ser valores numéricos")
                return
            
            # Get prediction from backend
            result = self.controller.backend.predict_vibration(distance, charge, lithology)
            
            if "Erro" in result or "Sem dados" in result:
                self.result_label.config(text=f"⚠️ {result}", fg='#e74c3c')
            else:
                self.result_label.config(text=f"✅ Vibração prevista: {result}", fg='#27ae60')
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Ocorreu um erro: {str(e)}")

class ModernDatabasePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f0f2f5')
        self.controller = controller
        
        # Main container
        main_container = tk.Frame(self, bg='#f0f2f5')
        main_container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Header section
        header_frame = tk.Frame(main_container, bg='#f0f2f5')
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Title
        title_label = tk.Label(header_frame,
                              text="📊 Atualização do Banco de Dados",
                              font=("Arial", 24, "bold"),
                              fg='#2c3e50',
                              bg='#f0f2f5')
        title_label.pack(side="left")
        
        # Back button
        back_btn = tk.Button(header_frame,
                            text="🔙 Voltar",
                            font=("Arial", 12, "bold"),
                            bg='#95a5a6',
                            fg='white',
                            relief='flat',
                            padx=20,
                            pady=10,
                            cursor='hand2',
                            command=lambda: controller.show_frame(ModernPredictionPage))
        back_btn.pack(side="right")
        
        # Input card
        input_card = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        input_card.pack(fill="x", pady=(0, 20))
        
        # Input card header
        input_header = tk.Frame(input_card, bg='#9b59b6', height=50)
        input_header.pack(fill="x")
        input_header.pack_propagate(False)
        
        input_title = tk.Label(input_header,
                              text="➕ Adicionar Novos Dados",
                              font=("Arial", 14, "bold"),
                              fg='white',
                              bg='#9b59b6')
        input_title.pack(expand=True)
        
        # Input fields
        input_section = tk.Frame(input_card, bg='white')
        input_section.pack(fill="x", padx=30, pady=20)
        
        # Create input grid
        self.create_input_grid(input_section)
        
        # Data display card
        display_card = tk.Frame(main_container, bg='white', relief='solid', bd=1)
        display_card.pack(fill="both", expand=True)
        
        # Display card header
        display_header = tk.Frame(display_card, bg='#34495e', height=50)
        display_header.pack(fill="x")
        display_header.pack_propagate(False)
        
        display_title = tk.Label(display_header,
                                text="📋 Dados Existentes",
                                font=("Arial", 14, "bold"),
                                fg='white',
                                bg='#34495e')
        display_title.pack(expand=True)
        
        # Data display
        self.create_data_display(display_card)
    
    def create_input_grid(self, parent):
        """Create the input grid with modern styling"""
        # Create 2x2 grid for inputs
        fields = [
            ("📏 Distância (m):", 0, 0),
            ("⚡ Carga de espera (kg):", 0, 2),
            ("📊 Vibração (mm/s):", 1, 0),
            ("🗿 Litologia:", 1, 2)
        ]
        
        self.entries = {}
        
        for field_name, row, col in fields:
            label = tk.Label(parent,
                           text=field_name,
                           font=("Arial", 11, "bold"),
                           fg='#2c3e50',
                           bg='white')
            label.grid(row=row, column=col, sticky="w", pady=10, padx=(0, 10))
            
            entry = tk.Entry(parent,
                           font=("Arial", 11),
                           relief='solid',
                           bd=2,
                           bg='#ecf0f1')
            entry.grid(row=row, column=col+1, sticky="ew", pady=10, padx=(0, 20), ipady=6)
            
            # Store entries for later access
            key = field_name.split()[1].lower()  # Extract key from emoji label
            self.entries[key] = entry
        
        # Configure grid weights
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        
        # Save button
        button_frame = tk.Frame(parent, bg='white')
        button_frame.grid(row=2, column=0, columnspan=4, pady=20)
        
        save_btn = tk.Button(button_frame,
                           text="💾 SALVAR NO BANCO DE DADOS",
                           font=("Arial", 14, "bold"),
                           bg='#e67e22',
                           fg='white',
                           relief='flat',
                           padx=30,
                           pady=12,
                           cursor='hand2',
                           command=self.save_to_database)
        save_btn.grid(row=0,column=0,padx=10)
        #save_btn.pack()

        save_btn_csv = tk.Button(button_frame,
                           text="📁 Importar CSV/Excel",
                           font=("Arial", 14, "bold"),
                           bg="#22e639",
                           fg='white',
                           relief='flat',
                           padx=30,
                           pady=12,
                           cursor='hand2',
                           command=self.save_to_database_csv)
        save_btn_csv.grid(row=0,column=1,padx=10)
        #save_btn_csv.pack()
    
    def create_data_display(self, parent):
        """Create a modern data display"""
        display_frame = tk.Frame(parent, bg='white')
        display_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create treeview with modern styling
        columns = ('ID', 'Distância (m)', 'Carga (kg)', 'Vibração (mm/s)', 'Litologia')
        self.tree = ttk.Treeview(display_frame, columns=columns, show='headings', height=10)
        
        # Define headings and column widths
        column_widths = [50, 120, 120, 140, 120]
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[i], anchor='center')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack elements
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Control buttons
        button_frame = tk.Frame(display_frame, bg='white')
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        refresh_btn = tk.Button(button_frame,
                              text="🔄 Atualizar Lista",
                              font=("Arial", 10, "bold"),
                              bg='#3498db',
                              fg='white',
                              relief='flat',
                              padx=15,
                              pady=8,
                              cursor='hand2',
                              command=self.load_data)
        refresh_btn.pack(side="left", padx=5)
        
        clear_btn = tk.Button(button_frame,
                            text="🗑️ Limpar Campos",
                            font=("Arial", 10, "bold"),
                            bg='#e74c3c',
                            fg='white',
                            relief='flat',
                            padx=15,
                            pady=8,
                            cursor='hand2',
                            command=self.clear_fields)
        clear_btn.pack(side="left", padx=5)
        
        # Load initial data
        self.load_data()
    
    def load_data(self):
        """Load data from database into treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            data = self.controller.backend.get_all_data()
            for row in data:
                # Format the data for display
                formatted_row = (
                    row[0],  # ID
                    f"{row[1]:.2f}",  # Distance
                    f"{row[2]:.2f}",  # Charge
                    f"{row[3]:.2f}",  # Vibration
                    row[4]  # Lithology
                )
                self.tree.insert('', 'end', values=formatted_row)
                
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao carregar dados: {str(e)}")
    
    def clear_fields(self):
        """Clear all input fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def save_to_database(self):
        """Save the input data to the database"""
        try:
            # Get values from entries
            distance = self.entries['distância'].get()
            charge = self.entries['carga'].get()
            vibration = self.entries['vibração'].get()
            lithology = self.entries['litologia:'].get()
            
            # Validate inputs
            if not all([distance, charge, vibration, lithology]):
                messagebox.showerror("❌ Erro", "Por favor, preencha todos os campos")
                return
            
            try:
                distance = float(distance)
                charge = float(charge)
                vibration = float(vibration)
                if distance <= 0 or charge <= 0 or vibration < 0:
                    messagebox.showerror("❌ Erro", "Valores inválidos")
                    return
            except ValueError:
                messagebox.showerror("❌ Erro", "Distância, carga e vibração devem ser valores numéricos")
                return
            
            # Save to database using backend
            success = self.controller.backend.save_data(distance, charge, vibration, lithology)
            
            if success:
                messagebox.showinfo("✅ Sucesso", "Dados salvos com sucesso!")
                self.controller.backend.calculate_k_factor() # salva os dados e recalcula todos as constantes
                self.clear_fields()
                self.load_data()
                # Update lithology options in prediction page
                self.controller.frames[ModernPredictionPage].update_lithology_options()
            else:
                messagebox.showerror("❌ Erro", "Erro ao salvar dados")
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Ocorreu um erro: {str(e)}")

    def save_to_database_csv(self):
        """Import data from CSV or Excel file and save to database"""
        try:
            # Open file dialog to select CSV or Excel file
            file_path = filedialog.askopenfilename(
                title="Selecionar arquivo CSV ou Excel",
                filetypes=[
                    ("Excel files", "*.xlsx *.xls"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ]
            )
            
            if not file_path:
                return  # User cancelled file selection
            
            # Show loading message
            loading_window = tk.Toplevel(self)
            loading_window.title("Importando dados...")
            loading_window.geometry("300x100")
            loading_window.configure(bg='#f0f2f5')
            loading_window.transient(self)
            loading_window.grab_set()
            
            # Center the loading window
            loading_window.geometry("+%d+%d" % (self.winfo_rootx() + 250, self.winfo_rooty() + 250))
            
            loading_label = tk.Label(loading_window, 
                                   text="📂 Carregando arquivo...", 
                                   font=("Arial", 12),
                                   bg='#f0f2f5')
            loading_label.pack(expand=True)
            
            # Update the window to show loading message
            loading_window.update()
            
            # Read the file based on extension
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'csv':
                # Try different encodings for CSV files
                encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                df = None
                
                for encoding in encodings:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                
                if df is None:
                    raise Exception("Não foi possível ler o arquivo CSV. Verifique a codificação.")
                    
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                raise Exception("Formato de arquivo não suportado. Use CSV ou Excel.")
            
            loading_label.config(text="📊 Processando dados...")
            loading_window.update()
            
            # Validate required columns
            required_columns = ['distancia', 'carga_espera', 'vibracao', 'litologia']
            df_columns_lower = [col.lower().strip() for col in df.columns]
            
            # Create column mapping (case insensitive)
            column_mapping = {}
            missing_columns = []
            
            for req_col in required_columns:
                found = False
                for i, col in enumerate(df_columns_lower):
                    # Check for exact match or common variations
                    if (req_col in col or 
                        col in req_col or
                        (req_col == 'distancia' and ('dist' in col or 'distance' in col)) or
                        (req_col == 'carga_espera' and ('carga' in col or 'charge' in col or 'peso' in col)) or
                        (req_col == 'vibracao' and ('vibr' in col or 'vibration' in col)) or
                        (req_col == 'litologia' and ('lito' in col or 'lithology' in col or 'rock' in col))):
                        column_mapping[req_col] = df.columns[i]
                        found = True
                        break
                
                if not found:
                    missing_columns.append(req_col)
            
            if missing_columns:
                loading_window.destroy()
                messagebox.showerror("❌ Erro", 
                                   f"Colunas obrigatórias não encontradas: {', '.join(missing_columns)}\n\n"
                                   f"Colunas disponíveis: {', '.join(df.columns)}\n\n"
                                   f"Certifique-se de que o arquivo contém as colunas:\n"
                                   f"- distancia (ou distance, dist)\n"
                                   f"- carga_espera (ou carga, charge, peso)\n"
                                   f"- vibracao (ou vibration, vibr)\n"
                                   f"- litologia (ou lithology, lito, rock)")
                return
            
            # Rename columns to match database schema
            df_renamed = df.rename(columns=column_mapping)
            
            loading_label.config(text="💾 Salvando no banco de dados...")
            loading_window.update()
            
            # Process and save data
            successful_imports = 0
            failed_imports = 0
            error_details = []
            
            for index, row in df_renamed.iterrows():
                try:
                    # Extract and validate data
                    distance = float(row[column_mapping['distancia']])
                    charge = float(row[column_mapping['carga_espera']])
                    vibration = float(row[column_mapping['vibracao']])
                    lithology = str(row[column_mapping['litologia']]).strip()
                    
                    # Validate values
                    if distance <= 0 or charge <= 0 or vibration < 0:
                        raise ValueError("Valores inválidos (negativos ou zero)")
                    
                    if not lithology or lithology.lower() in ['nan', 'null', '']:
                        raise ValueError("Litologia vazia")
                    
                    # Save to database
                    if self.controller.backend.save_data(distance, charge, vibration, lithology):
                        successful_imports += 1
                    else:
                        failed_imports += 1
                        error_details.append(f"Linha {index + 2}: Erro ao salvar no banco")
                        
                except Exception as e:
                    failed_imports += 1
                    error_details.append(f"Linha {index + 2}: {str(e)}")
            
            # Close loading window
            loading_window.destroy()
            
            # Show results
            if successful_imports > 0:
                result_message = f"✅ Importação concluída!\n\n"
                result_message += f"📊 Registros importados com sucesso: {successful_imports}\n"
                self.controller.backend.calculate_k_factor()
                
                if failed_imports > 0:
                    result_message += f"❌ Registros com erro: {failed_imports}\n\n"
                    result_message += "Detalhes dos erros:\n"
                    result_message += "\n".join(error_details[:10])  # Show first 10 errors
                    if len(error_details) > 10:
                        result_message += f"\n... e mais {len(error_details) - 10} erros"
                
                messagebox.showinfo("Importação de Dados", result_message)
                
                # Refresh data display if we're on the database page
                if hasattr(self.controller.frames[ModernDatabasePage], 'load_data'):
                    self.controller.frames[ModernDatabasePage].load_data()
                
                # Update lithology options in prediction page
                if hasattr(self.controller.frames[ModernPredictionPage], 'update_lithology_options'):
                    self.controller.frames[ModernPredictionPage].update_lithology_options()
                    
            else:
                error_message = f"❌ Nenhum registro foi importado!\n\n"
                error_message += f"Total de erros: {failed_imports}\n\n"
                error_message += "Primeiros erros:\n"
                error_message += "\n".join(error_details[:5])
                messagebox.showerror("Erro na Importação", error_message)
                
        except FileNotFoundError:
            messagebox.showerror("❌ Erro", "Arquivo não encontrado!")
        except pd.errors.EmptyDataError:
            messagebox.showerror("❌ Erro", "O arquivo está vazio!")
        except Exception as e:
            if 'loading_window' in locals():
                loading_window.destroy()
            messagebox.showerror("❌ Erro", f"Erro ao processar arquivo:\n{str(e)}")
    

if __name__ == "__main__":
    app = ModernVibrationApp()
    app.mainloop()