import math
import tkinter as t
from tkinter import messagebox

class Cal_OnGrid:
    def __init__(self, PowerConsume, PercentYield):
        self._PowerConsume = PowerConsume
        self._PercentYield = PercentYield
        InverterType = {"type1": [5, 17000], "type2" : [30,48000], "type3" : [50,135000]}
        self._sorted_InverterType = dict(sorted(InverterType.items(), key=lambda item: item[1][0]))

    def CalAvg_PowerConsume_Day(self): 
        Avg_PowerConsume_Day = self._PowerConsume / 30
        return round(Avg_PowerConsume_Day, 2)
    
    def Cal_KWp(self):
        KWp = self.CalAvg_PowerConsume_Day() * 1.2
        return round(KWp,2)
    
    def Cal_PanalAmount(self):
        PanelAmount = (self.Cal_KWp() * 1000) / 580
        return math.ceil(PanelAmount)
    
    def Cal_SolarCost(self): 
        SolarCost = self.Cal_PanalAmount() * 3500
        return round(SolarCost,2)
    
    def Cal_AreaRequire(self):
        AreaRequire = self.Cal_PanalAmount() * 3
        return round(AreaRequire,2)
    
    def Cal_InstallationCost(self):
        InstallationCost = self.Cal_PanalAmount() * 580
        return round(InstallationCost,2)
    
    def Cal_InverterCapacity(self):
        InverterCapacity = self.Cal_KWp() / 1.25
        return InverterCapacity
    
    def Cal_InverterCost_Type(self):
        InverterCapacity = self.Cal_InverterCapacity()
        for key, value in self._sorted_InverterType.items():
            if InverterCapacity  <= value[0]:
                return key, value[1], value[0]
        return False
    
    def Cal_EletricCost(self):
        if self._PowerConsume <= 150:
            if self._PowerConsume <= 15:
                EletricCost = (self._PowerConsume * 2.3488) + 38.22
            elif self._PowerConsume <= 25:
                EletricCost = 8.19 + (15 * 2.3488) + (self._PowerConsume - 15)
            elif self._PowerConsume <= 35:
                EletricCost = 8.19 + (15 * 2.3488) + (10 * 2.9882) + (self._PowerConsume - 25) * 3.2405
            elif self._PowerConsume <= 100:
                EletricCost = 8.19 + (15 * 2.3488) + (10 * 2.9882) + (10 * 3.2405) + (self._PowerConsume - 35) * 3.6237
            elif self._PowerConsume <= 150:
                EletricCost = 8.19 + (15 * 2.3488) + (10 * 2.9882) + (10 * 3.2405) + (65 * 3.6237) + (self._PowerConsume - 100) * 3.7171
        else:
            if self._PowerConsume <= 400:
                EletricCost = 38.22 + (150 * 3.2484) + (self._PowerConsume - 150) * 4.2218
            elif self._PowerConsume >= 400:
                EletricCost = 38.22 + (150 * 3.2484)  + (250 * 4.2218) + (self._PowerConsume - 400) * 4.4217

        Ft = self._PowerConsume * 0.2048
        vat = (EletricCost + Ft) * 0.07
        Sum = EletricCost + Ft + vat
        return Sum

    def Sum_TotalCost(self):
        if self.Cal_InverterCost_Type() == False:
            return False
        else:
            TotalCost = self.Cal_InstallationCost() + self.Cal_SolarCost() + self.Cal_InverterCost_Type()[1]
            return round(TotalCost,2)
    
    def Cal_Payback(self):
        TotalCost = self.Sum_TotalCost()
        if TotalCost == False:
            return False
        else:
            Payback = TotalCost / (self.Cal_EletricCost() * (self._PercentYield / 100))
            return round(Payback,2)
    
class Cal_OnGridBattery(Cal_OnGrid):
    def __init__(self, PowerConsume, PercentYield, UseHr):
        super().__init__(PowerConsume, PercentYield)
        self._UseHr = UseHr
        BatteryType = {"type1": [80, 3200], "type2" : [125,5900], "type3" : [160,8000]}
        self._sorted_BatteryType = dict(sorted(BatteryType.items(), key=lambda item: item[1][0]))

    def Cal_BatteryCapacity(self):
        BatteryCapacity = (self._PowerConsume * self._UseHr) / (48 * 0.6 * 0.85)
        return BatteryCapacity
    
    def Cal_BatteryCost_Type(self):
        BatterySize = self.Cal_BatteryCapacity()
        for key, value in self._sorted_BatteryType.items():
            if BatterySize <= value[0]:
                return key, value[1], value[0]
        return False

    def Sum_TotalCost(self):
        if self.Cal_InverterCost_Type() == False or self.Cal_BatteryCost_Type() == False:
            return False
        else:
            TotalCost = self.Cal_InstallationCost() + self.Cal_SolarCost() + self.Cal_InverterCost_Type()[1] + self.Cal_BatteryCost_Type()[1]
            return TotalCost
        
def valid_Number(value): #110-122 ทำให้ใส่ได้แค่ตัวเลข
    try:
        float(value)
        return True
    except ValueError:
        return False

def valid_DataType(P):
    if valid_Number(P) or P == "":
        return True
    else:
        root.bell()
        return False

def OnGrid_window():
    Cal_OnGrid_window.deiconify()
    root.withdraw()

def OnGridBattery_window():
    Cal_OnGridBattery_window.deiconify()
    root.withdraw() 

def ReturnMenu():
    Cal_OnGrid_window.withdraw()
    Cal_OnGridBattery_window.withdraw()
    root.deiconify()

def OnGrid_Result(_PowerConsume, _PercentYield):
    Cal_OnGrid_Obj = Cal_OnGrid(_PowerConsume,_PercentYield)
    Result_window = t.Toplevel(root)
    Result_window.title("Result")
    Result_window.config(bg="lightblue")
    Result_window.resizable(False, False)
    Result_window.geometry("500x400")

    message_label1 = t.Label(Result_window, text=f"ค่าเฉลี่ยใช้ไฟฟ้ารายวัน : {Cal_OnGrid_Obj.CalAvg_PowerConsume_Day()} หน่วย", bg="lightblue")
    message_label1.pack(pady=10, padx=10)

    message_label2 = t.Label(Result_window, text=f"จำนวนโซล่าเซลล์ : {Cal_OnGrid_Obj.Cal_PanalAmount()} แผง", bg="lightblue")
    message_label2.pack(pady=10, padx=10)

    message_label3 = t.Label(Result_window, text=f"ราคาโซล่าเซลล์จำนวน {Cal_OnGrid_Obj.Cal_PanalAmount()} แผง : {Cal_OnGrid_Obj.Cal_SolarCost()} บาท", bg="lightblue")
    message_label3.pack(pady=10, padx=20)

    message_label4 = t.Label(Result_window, text=f"ขนาดพื้นที่ใช้ในการติดตั้ง : {Cal_OnGrid_Obj.Cal_AreaRequire()} ตร.ม.", bg="lightblue")
    message_label4.pack(pady=10, padx=20)

    message_label5 = t.Label(Result_window, text=f"ราคาค่าติดตั้งโซล่าเซลล์ : {Cal_OnGrid_Obj.Cal_InstallationCost()} บาท", bg="lightblue")
    message_label5.pack(pady=10, padx=20)

    if Cal_OnGrid_Obj.Cal_InverterCost_Type() == False: # 160-161 ถ้ามีมีชนิดinverter ให้ขึ้นerror message หรือ 162 - 170 ถ้ามีชนิด inverter แสดงปกติ
        messagebox.showerror("Error Occur!", "ไม่พบชนิด Inverter ที่เหมาะสม")
    else:
        message_label6 = t.Label(Result_window, text=f"ชนิดและราคา Inverter : {Cal_OnGrid_Obj.Cal_InverterCost_Type()[0]}({Cal_OnGrid_Obj.Cal_InverterCost_Type()[2]} kWp) ราคา : {Cal_OnGrid_Obj.Cal_InverterCost_Type()[1]} บาท", bg="lightblue")
        message_label6.pack(pady=10, padx=20)

        message_label7 = t.Label(Result_window, text=f"ค่าใช้จ่ายทั้งหมด : {Cal_OnGrid_Obj.Sum_TotalCost()} บาท", bg="lightblue")
        message_label7.pack(pady=10, padx=20)

        message_label8 = t.Label(Result_window, text=f"ระยะเวลาคืนทุน(เดือน) : {Cal_OnGrid_Obj.Cal_Payback()} เดือน", bg="lightblue")
        message_label8.pack(pady=10, padx=20)

    close_button = t.Button(Result_window, text="Close", command=Result_window.destroy)
    close_button.pack(pady=10)

def OnGridBattery_Result(_PowerConsume, _PercentYield, _UseHr):
    Cal_OnGridBattery_Obj = Cal_OnGridBattery(_PowerConsume,_PercentYield,_UseHr)
    Result_window = t.Toplevel(root)
    Result_window.title("Result")
    Result_window.config(bg="lightblue")
    Result_window.resizable(False, False)
    Result_window.geometry("500x450")

    message_label1 = t.Label(Result_window, text=f"ค่าเฉลี่ยใช้ไฟฟ้ารายวัน : {Cal_OnGridBattery_Obj.CalAvg_PowerConsume_Day()} หน่วย", bg="lightblue")
    message_label1.pack(pady=10)

    message_label2 = t.Label(Result_window, text=f"จำนวนโซล่าเซลล์ : {Cal_OnGridBattery_Obj.Cal_PanalAmount()} แผง", bg="lightblue")
    message_label2.pack(pady=10, padx=10)

    message_label3 = t.Label(Result_window, text=f"ราคาโซล่าเซลล์จำนวน {Cal_OnGridBattery_Obj.Cal_PanalAmount()} แผง : {Cal_OnGridBattery_Obj.Cal_SolarCost()} บาท", bg="lightblue")
    message_label3.pack(pady=10, padx=20)

    message_label4 = t.Label(Result_window, text=f"ขนาดพื้นที่ใช้ในการติดตั้ง : {Cal_OnGridBattery_Obj.Cal_AreaRequire()} ตร.ม.", bg="lightblue")
    message_label4.pack(pady=10, padx=20)

    message_label5 = t.Label(Result_window, text=f"ราคาค่าติดตั้งโซล่าเซลล์ : {Cal_OnGridBattery_Obj.Cal_InstallationCost()} บาท", bg="lightblue")
    message_label5.pack(pady=10, padx=20)

    if Cal_OnGridBattery_Obj.Cal_InverterCost_Type() == False or Cal_OnGridBattery_Obj.Cal_BatteryCost_Type() == False: #198-199
        messagebox.showerror("Error Occur!", "ไม่พบชนิด Inverter หรือ แบตเตอร์รี่ ที่เหมาะสม")
    else:
        message_label5 = t.Label(Result_window, text=f"ชนิดและราคาแบตเตอร์รี่ : {Cal_OnGridBattery_Obj.Cal_BatteryCost_Type()[0]}({Cal_OnGridBattery_Obj.Cal_BatteryCost_Type()[2]} Ah) (ราคา : {Cal_OnGridBattery_Obj.Cal_BatteryCost_Type()[1]} บาท)", bg="lightblue")
        message_label5.pack(pady=10, padx=20)
        
        message_label6 = t.Label(Result_window, text=f"ชนิดและราคา Inverter : {Cal_OnGridBattery_Obj.Cal_InverterCost_Type()[0]}({Cal_OnGridBattery_Obj.Cal_InverterCost_Type()[2]} kWp) ราคา : {Cal_OnGridBattery_Obj.Cal_InverterCost_Type()[1]} บาท", bg="lightblue")
        message_label6.pack(pady=10, padx=20)

        message_label7 = t.Label(Result_window, text=f"ค่าใช้จ่ายทั้งหมด : {Cal_OnGridBattery_Obj.Sum_TotalCost()} บาท", bg="lightblue")
        message_label7.pack(pady=10, padx=20)

        message_label8 = t.Label(Result_window, text=f"ระยะเวลาคืนทุน(เดือน) : {Cal_OnGridBattery_Obj.Cal_Payback()} เดือน", bg="lightblue")
        message_label8.pack(pady=10, padx=20)

    close_button = t.Button(Result_window, text="Close", command=Result_window.destroy)
    close_button.pack(pady=10)
def get_value_OnGrid():
    PowerConsume = Entry_PowerConsume_OnGrid.get()
    PercentYield = Entry_PercentYield_OnGrid.get()
    if valid_Number(PowerConsume) == False or valid_Number(PercentYield) == False or float(PercentYield) > 100 or float(PercentYield) <= 0 or float(PowerConsume) < 1:
        print("error") 
        messagebox.showerror("Error Occur!", "ข้อมูลไม่ถูกต้อง สาเหตุอาจมาจาก:\n1.ค่าเฉลี่ยการใช้ไฟต่ำกว่า 1\n2.การกรอกเปอร์เซนต์การทำงานต้องอยู่ในช่วง มากกว่า0-100\n3.กรอกข้อมูลไม่ครบถ้วน")
    else:
        _PowerConsume = float(PowerConsume)
        _PercentYield = float(PercentYield)
        OnGrid_Result(_PowerConsume, _PercentYield)

def get_value_OnGridBattery():
    PowerConsume = Entry_PowerConsume_OnGridBattery.get()
    PercentYield = Entry_PercentYield_OnGridBattery.get()
    UseHr = Entry_HourSupply.get()
    if valid_Number(PowerConsume) == False or valid_Number(PercentYield) == False or valid_Number(UseHr) == False or float(PercentYield) > 100 or float(PercentYield) <= 0 or float(UseHr) <= 0 or float(UseHr) > 24 or float(PowerConsume) < 1:
        print("Error")
        messagebox.showerror("Error Occur!", "ข้อมูลไม่ถูกต้อง สาเหตุอาจมาจาก:\n1.ค่าเฉลี่ยการใช้ไฟต่ำกว่า 1\n2.การกรอกเปอร์เซนต์การทำงานต้องอยู่ในช่วง มากกว่า0-100\n3.การกรอกจำนวนชัวโมงต้องอยู่ในช่วง 1-24\n4.กรอกข้อมูลไม่ครบถ้วน")
    else:
        _PowerConsume = float(PowerConsume)
        _PercentYield = float(PercentYield)
        _UseHr =  float(UseHr)
        OnGridBattery_Result(_PowerConsume, _PercentYield, _UseHr)
    

root = t.Tk()
root.resizable(False, False)
root.config(bg="lightblue")
root.title("Solar System Assistance")
root.geometry("600x500")

label = t.Label(root, text="Solar System\nAssistance", font=("Arial", 30), bg="lightblue")
label.pack(padx=90, pady=10)

button_Cal_OnGrid = t.Button(root, text="On Grid", command=OnGrid_window, width=25, height=2, font=("Arial", 12))
button_Cal_OnGrid.pack(padx=90, pady=20)

button_Cal_OnGridBattery = t.Button(root, text="On Grid with battery", command=OnGridBattery_window, width=25, height=2, font=("Arial", 12))
button_Cal_OnGridBattery.pack(padx=90, pady=20)

exit_button = t.Button(root, text="Exit", command=root.quit, width=25, height=2, font=("Arial", 12))
exit_button.pack(padx=90, pady=20)

Cal_OnGrid_window = t.Toplevel()
Cal_OnGrid_window.title("On Gride without battery")
Cal_OnGrid_window.geometry("400x200")
Cal_OnGrid_window.resizable(False, False)
Cal_OnGrid_window.config(bg="lightblue")
Cal_OnGrid_window.withdraw()
Cal_OnGrid_window.protocol("WM_DELETE_WINDOW", ReturnMenu)
validate_cmd1 = Cal_OnGrid_window.register(valid_DataType)

label = t.Label(Cal_OnGrid_window, text="ไฟฟ้าที่ใช้เฉลี่ยแต่ละเดือน(Unit,kW) :", font=("Arial", 10), bg="lightblue")
label.place(x=20, y=25)

Entry_PowerConsume_OnGrid = t.Entry(Cal_OnGrid_window, validate="key", validatecommand=(validate_cmd1, "%P"))
Entry_PowerConsume_OnGrid.place(x=220, y=27)

label = t.Label(Cal_OnGrid_window, text="เปอร์เซนการทำงานของโซล่าเซลล์(1-100%) :", font=("Arial", 10), bg="lightblue")
label.place(x=20, y=60)

Entry_PercentYield_OnGrid = t.Entry(Cal_OnGrid_window, validate="key", validatecommand=(validate_cmd1, "%P"))
Entry_PercentYield_OnGrid.place(x=250, y=63)

button_Cal = t.Button(Cal_OnGrid_window, text="Calculate", command=get_value_OnGrid)
button_Cal.place(x=165, y=115)

return_button = t.Button(Cal_OnGrid_window, text="Return to Main Menu", command=ReturnMenu)
return_button.place(x=135, y=150)
#______________________________________________________________________________________________________________

Cal_OnGridBattery_window = t.Toplevel()
Cal_OnGridBattery_window.title("On Gride with battery")
Cal_OnGridBattery_window.geometry("400x200")
Cal_OnGridBattery_window.resizable(False, False)
Cal_OnGridBattery_window.config(bg="lightblue")
Cal_OnGridBattery_window.withdraw()
Cal_OnGridBattery_window.protocol("WM_DELETE_WINDOW", ReturnMenu)
validate_cmd2 = Cal_OnGridBattery_window.register(valid_DataType)

label = t.Label(Cal_OnGridBattery_window, text="ไฟฟ้าที่ใช้เฉลี่ยแต่ละเดือน(Unit, kW) :", font=("Arial", 10), bg="lightblue")
label.place(x=20, y=10)
Entry_PowerConsume_OnGridBattery = t.Entry(Cal_OnGridBattery_window, validate="key", validatecommand=(validate_cmd2, "%P"))
Entry_PowerConsume_OnGridBattery.place(x=220, y=12)

label = t.Label(Cal_OnGridBattery_window, text="เปอร์เซนการทำงานของโซล่าเซลล์(1-100%) :", font=("Arial", 10), bg="lightblue")
label.place(x=20, y=45)
Entry_PercentYield_OnGridBattery = t.Entry(Cal_OnGridBattery_window, validate="key", validatecommand=(validate_cmd2, "%P"))
Entry_PercentYield_OnGridBattery.place(x=250, y=48)

label = t.Label(Cal_OnGridBattery_window, text="ชัวโมงการทำงานของแบตเตอร์รี่ :", font=("Arial", 10), bg="lightblue")
label.place(x=20, y=80)
Entry_HourSupply = t.Entry(Cal_OnGridBattery_window, validate="key", validatecommand=(validate_cmd2, "%P"))
Entry_HourSupply.place(x=190, y=82)

button_Cal = t.Button(Cal_OnGridBattery_window, text="Calculate", command=get_value_OnGridBattery)
button_Cal.place(x=165, y=125)

return_button = t.Button(Cal_OnGridBattery_window, text="Return to Main Menu", command=ReturnMenu)
return_button.place(x=135, y=160)

root.mainloop()
