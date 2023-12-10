# ONLY INDIAN CURRENCY , AMOUNT(RUPPE) , DISTANCE(KM) AND ADDRESS SUPPORTED  
from customtkinter import filedialog,CTkScrollbar,CTkLabel,CTkFrame,CTkButton,CTkFont,CTkScrollableFrame
from pathlib import Path
from tkinter import ttk
from cosine import cosine_similarity
from message_box import Messagebox
import customtkinter
import json
import os
import requests
import io
def convert_to_string(keys,option):
    if option=='date' or option=='address':
       return ', '.join([str(key) for key in keys])
    elif option=='amount':
       return '₹, '.join([str(key) for key in keys])
    elif option=='distance':
       return ' km, '.join([str(key) for key in keys])    
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.AppConfigure()
        self.treeViewConfigure()
        self.addSideBar()
        self.addTable()
        self.addInvoiceTestFrame()
        self.LABEL_FILE='/'
        self.TEST_DIR='/'
        self.total_correct=[0,0,0,0]
        self.total_actual=[0,0,0,0]
        self.API=None
 
    def AppConfigure(self):
        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green"
        screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.title("Ess Conveyance Testing App( Tally Solutions) - Made with ❤️ in India")
        self.geometry(f"{screen_width}x{self.screen_height}")

    def treeViewConfigure(self):
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10),background="#2a2d2e",foreground="white",rowheight=25,fieldbackground="#343638",bordercolor="#343638",borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat")
        style.map("Treeview.Heading",background=[('active', '#3484F0')])    

    def addSideBar(self):
        self.sidebar_frame = CTkFrame(self, corner_radius=5)
        self.sidebar_frame.grid(sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        logo_label = CTkLabel(self.sidebar_frame, text="Tally Solutions\nESS Conveyance Test", font=CTkFont(size=20, weight="bold"))
        logo_label.grid(row=0, column=0, padx=0, pady=5)
        self.folderSetUP()
        self.fileSetUP()
        api_button = CTkButton(self.sidebar_frame,text='Input API',command=self.get_input_api)
        api_button.grid(row=4, column=0, padx=0, pady=10,sticky="e")        
        sidebar_button_3 = CTkButton(self.sidebar_frame,text='Start Test',command=self.startInvoiceProcessing,fg_color="green")
        sidebar_button_3.grid(row=5, column=0, padx=0, pady=10,sticky="e")
            
            
    def folderSetUP(self):
        directory_button = CTkButton(self.sidebar_frame,text='Choose Dataset Folder',command=self.open_dir)
        directory_button.grid(row=1, column=0, padx=0, pady=5, sticky="w")
        test_folder_path_button=CTkButton(self.sidebar_frame,text='Show Folder Path',command=self.displayFolderPath,fg_color="green")
        test_folder_path_button.grid(row=1, column=1, padx=0, pady=0,sticky="w")

    def open_dir(self):
        self.TEST_DIR=filedialog.askdirectory()

    def displayFolderPath(self):
        Messagebox("Please verify that path is correct!",self.TEST_DIR)

    def fileSetUP(self):
        file_button = CTkButton(self.sidebar_frame,text='Choose Label File',command=self.open_file)
        file_button.grid(row=3, column=0, padx=0, pady=10,sticky="w")
        test_file_path_button=CTkButton(self.sidebar_frame,text='Show File Path',command=self.displayFilePath,fg_color="green")
        test_file_path_button.grid(row=3, column=1, padx=0, pady=10,sticky="w")
    
    def open_file(self):
        self.LABEL_FILE=filedialog.askopenfilename()

    def displayFilePath(self):
        Messagebox("Please verify that path is correct!",self.LABEL_FILE)

    def compare(self,correct,computed,index): #return value [is_valid,computed key ]
        #Algorithm to check if computed value may be the correct value
        if correct=='':
            return ['⬜','']
        self.total_actual[index]+=1
        if len(computed)==0:
            return ['❌','']
        if correct in computed:
            self.total_correct[index]+=1
            return ['✔',correct]
        try:
         return ['❌',computed[0]]
        except:
         print('computed',computed)
    
    def compare_address(self,correct,computed,index):
        if len(correct)==0:
           return ['⬜']
        self.total_actual[index]+=1
        length=len(computed)
        if length==0:
           return ['❌']
        best_similar_address=[] # atmost 3 or 4 address could be present in invoice
        total_accuracy=0
        for correct_address in correct:
            best_similarity_address_index=0
            best_similarity=0.0        
            for i in range(length):
                similarity=cosine_similarity(computed[i],correct_address)
                if similarity>best_similarity:
                    best_similarity_address_index=i 
                    best_similarity=similarity
            best_similar_address.append(computed[best_similarity_address_index])
            total_accuracy+=best_similarity
        total_accuracy/=len(correct) #store mean of total accuracy
        self.total_correct[index]+=total_accuracy #add the mean correctness
        result=['✅' if total_accuracy>=.8 else '❌']
        result.extend(best_similar_address)
        return result

    def computeAccuracy(self,index):
        if self.total_actual[index]==0:
            return 0
        return round(self.total_correct[index]/self.total_actual[index]*100,2)

    def startInvoiceProcessing(self):
        if  Path(self.LABEL_FILE).suffix != '.json':
             Messagebox("Unknown file","Choose a labeled json test file!")
             return
        if  self.API == None or self.API =='':
             Messagebox("","please enter a valid api!")
             return
        self.resetTable()
        file_names=os.listdir(self.TEST_DIR)
        size=len(file_names)
        labeled_data=json.load(open(self.LABEL_FILE))
        for i in range(size):
            if Path(file_names[i]).suffix != '.pdf' or (file_names[i] not in labeled_data) :
               continue
            files={'file':(f'{file_names[i]}', open(f'{self.TEST_DIR}/{file_names[i]}', 'rb'), 'application/pdf'),'Content-Type': 'multipart/form-data'}
            response = requests.post(self.API, files=files)
            if response.status_code != 200:
                print('Error uploading PDF:', response.status_code,'response:',response.text)
                continue
            tags=[]
            invoice_data= json.loads(response.text)
            invoice_data['date']=list(invoice_data['date'])
            invoice_data['distance']=list(invoice_data['distance'])
            invoice_data['amount']=list(invoice_data['amount'])
            invoice_data['address']=list(invoice_data['address'])
            date=self.compare(labeled_data[file_names[i]]['date'],invoice_data['date'],0)
            tags.extend([labeled_data[file_names[i]]['date'],convert_to_string(invoice_data['date'],'date')])
            distance=self.compare(labeled_data[file_names[i]]['distance'],invoice_data['distance'],1)
            tags.extend([labeled_data[file_names[i]]['distance'],convert_to_string(invoice_data['distance'],'distance')])
            amount=self.compare(labeled_data[file_names[i]]['amount'],invoice_data['amount'],2)
            tags.extend([labeled_data[file_names[i]]['amount'],convert_to_string(invoice_data['amount'],'amount')])
            address=self.compare_address(labeled_data[file_names[i]]['address'],invoice_data['address'],3)
            tags.extend(labeled_data[file_names[i]]['address'])            
            tags.extend(address[1:])
            self.table.insert(parent='',index=i,values=(file_names[i],date[0],distance[0],amount[0],address[0]),tags=tags)
            self.table.update() #Not necessary as table values can be all updated at once and shown to the user after all the process.
        #Set the accuracy for each field
        self.date.configure(text=f'Date {self.computeAccuracy(0)}% Accurate')
        self.distance.configure(text=f'Distance {self.computeAccuracy(1)}% Accurate')
        self.amount.configure(text=f'Amount {self.computeAccuracy(2)}% Accurate')
        self.address.configure(text=f'Address {self.computeAccuracy(3)}% Accurate')

    def resetTable(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for i in range(4):
           self.total_correct[i]=0
           self.total_actual[i]=0

    def addTable(self):
        self.frame_right =CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        columns = ('Invoice', 'Date', 'Distance', 'Amount','Address')
        self.table = ttk.Treeview(master=self.frame_right,
                              columns=columns,
                              height=20,
                              selectmode='browse',
                              show='headings')
        scrollbar = CTkScrollbar(self.frame_right, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set) 
        scrollbar.place(x=510,y=80)
         
        self.table.column("#1", anchor="c", minwidth=100, width=100)
        self.table.column("#2", anchor="c", minwidth=100, width=100)
        self.table.column("#3", anchor="c", minwidth=110, width=110)
        self.table.column("#4", anchor="c", minwidth=100, width=100)
        self.table.column("#5", anchor="c", minwidth=100, width=100)

        self.table.heading('Invoice', text='Invoice')
        self.table.heading('Date', text='Date')
        self.table.heading('Distance', text='Distance (km)')
        self.table.heading('Amount', text='Amount')
        self.table.heading('Address', text='Address')

        self.table.grid(row=0, column=0, sticky='nsew', padx=10, pady=50)
        self.table.bind('<Motion>', 'break')
        self.table.bind("<<TreeviewSelect>>",self.on_row_click)

    def addInvoiceTestFrame(self):
        invoice_frame = CTkScrollableFrame(master=self.frame_right,border_color="#343638",width=420,height=int(self.screen_height*.85))
        invoice_frame.grid(row=0, column=3, sticky="nswe", padx=5, pady=2) 
        self.date=CTkLabel(invoice_frame, text="Date",font=("Arial", 25, "bold"),text_color="white")
        self.date.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.computedDate=CTkLabel(invoice_frame, text="Computed date:date-month-year",font=("Courier", 15, "bold"))
        self.computedDate.grid(row=1, column=0, padx=20, pady=0,sticky="w")        
        self.actualDate=CTkLabel(invoice_frame,text="Actual date:date-month-year",font=("Courier",15,"bold"),text_color="white")
        self.actualDate.grid(row=2,column=0,padx=20,pady=0,stick="w")

        self.distance=CTkLabel(invoice_frame, text="Distance",font=("Arial", 25, "bold"),text_color="white")
        self.distance.grid(row=4, column=0, padx=20, pady=20)
        self.computedDistance=CTkLabel(invoice_frame, text="Computed Distance:Example 10 km",font=("Courier", 15, "bold"),text_color="white")
        self.computedDistance.grid(row=5, column=0, padx=20, pady=0,sticky="w")        
        self.actualDistance=CTkLabel(invoice_frame,text="Actual Distance:Example 10 km",font=("Courier",15,"bold"),text_color="white")
        self.actualDistance.grid(row=6,column=0,padx=20,pady=0,sticky="w")

        self.amount=CTkLabel(invoice_frame, text="Amount",font=("Arial", 25, "bold"),text_color="white")
        self.amount.grid(row=7, column=0, padx=20, pady=20)
        self.computedAmount=CTkLabel(invoice_frame,text="Computed Amount:Example ₹20",font=("Courier", 15, "bold"),text_color="white")
        self.computedAmount.grid(row=8, column=0, padx=20, pady=0,sticky="w")       
        self.actualAmount=CTkLabel(invoice_frame, text="Actual Amount: Example ₹20",font=("Courier", 15, "bold"),text_color="white")
        self.actualAmount.grid(row=9, column=0, padx=20, pady=0,sticky="w")
        
        self.address=CTkLabel(invoice_frame, text="Address",font=("Arial", 25, "bold"),text_color="white")
        self.address.grid(row=10, column=0, padx=20, pady=20)
        self.computedAddress=CTkLabel(invoice_frame,text="Computed Address:\n(1) [Recipient's Name], [Street Address], [City], [State], [PIN Code], India",font=("Courier", 15, "bold"),text_color="white",justify="left",wraplength=400)
        self.computedAddress.grid(row=11, column=0, padx=20, pady=0,sticky="w")        
        self.actualAddress=CTkLabel(invoice_frame, text="\nActual Address:\n(1)[Recipient's Name], [Street Address], [City], [State], [PIN Code], India",font=("Courier", 15, "bold"),text_color="white",justify="left",wraplength=400)
        self.actualAddress.grid(row=12, column=0, padx=20, pady=0,sticky="w")
        
    def open_file(self):
        self.LABEL_FILE=filedialog.askopenfilename()
 
    def open_dir(self):
        self.TEST_DIR=filedialog.askdirectory()
 
    def on_row_click(self,event):
         row=self.table.selection()
         if len(row)==0:
            return
         row_id=row[0]
         data=self.table.item(row_id,'tags')
         self.actualDate.configure(text=f'Actual Date:{data[0]}')
         self.computedDate.configure(text=f'Computed Date:{data[1]}')
         self.actualDistance.configure(text=f'Actual Distance:{data[2]} Km')
         self.computedDistance.configure(text=f'Computed Distance:{data[3]} Km')
         self.actualAmount.configure(text=f'Actual Amount: ₹{data[4]}')
         self.computedAmount.configure(text=f'Computed Amount:₹{data[5]}')
         tags_done=6
         actual_address='Actual Address:'
         computed_address='Computed Address:'
         AddressArrayLength=(len(data)-tags_done)//2
         count=1
         for i in range(tags_done,AddressArrayLength+tags_done):
            actual_address+=f'\n({count}).{data[i]}'
            count+=1
         count=1
         for i in range(tags_done+AddressArrayLength,len(data)):
            computed_address+=f'\n({count}).{data[i]}'
            count+=1
         self.actualAddress.configure(text=actual_address)
         self.computedAddress.configure(text=computed_address)
         
    def get_input_api(self):
        dialog = customtkinter.CTkInputDialog(text="Please enter the API key or URL", title="CTkInputDialog")
        self.API=dialog.get_input()

if __name__ == "__main__":
    app = App()
    app.mainloop()
