import time
import shutil
import os
import tkinter as tk
import sys
import win32service
import win32serviceutil

# قائمة الخدمات التي ترغب في إيقافها وتعطيلها
services = [
    "GoogleChromeElevationService",
    "SCardSvr",
    'BDESVC',
    'Netlogon',
    'SessionEnv',
    'TermService',
    'seclogon',
    'SysMain',
    'SgrmBroker',
    'SDRSVC',
    'WbioSrvc',
    'XboxGipSvc',
    'XblAuthManager',
    'XblGameSave',
    'XboxNetApiSvc'
]

def stop_service(service_name):
    try:
        handle = win32serviceutil.SmartOpenService(service_name)
        win32serviceutil.StopService(service_name)
        return f"Service {service_name} stopped successfully."
    except Exception as e:
        return f"Failed to stop {service_name}: {e}"

def disable_service(service_name):
    try:
        win32serviceutil.ChangeServiceConfig(service_name, startType=win32service.SERVICE_DISABLED)
        return f"Service {service_name} disabled successfully."
    except Exception as e:
        return f"Failed to disable {service_name}: {e}"

def disable_scheduled_task(task_path, task_name):
    # تعطيل المهمة
    try:
        os.system(f"schtasks /Change /TN \"{task_path}\\{task_name}\" /DISABLE")
        return f"Task {task_path}\\{task_name} disabled successfully."
    except Exception as e:
        return f"Failed to disable task {task_path}\\{task_name}: {e}"

def delete_temp_files():
    temp_dirs = [
        os.environ.get('TEMP', ''),  # Get the %TEMP% directory
        os.path.join(os.environ.get('SystemRoot', ''), 'Temp'),  # System temp directory
        os.path.join(os.environ.get('SystemRoot', ''), 'Prefetch')  # Prefetch directory
    ]

    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                print(f"Cleared {temp_dir}")
            except Exception as e:
                print(f"Failed to clear {temp_dir}: {e}")

def restart_computer():
    try:
        # إعادة تشغيل الجهاز
        os.system("shutdown /r /t 0")
    except Exception as e:
        progress_label.config(text=f"Failed to restart computer: {e}")
        window.update()

def close_application():
    # إغلاق التطبيق
    window.destroy()

def run_tasks():
    # إيقاف وتعطيل الخدمات
    for service in services:
        result = stop_service(service)
        progress_label.config(text=result)
        window.update()

        result = disable_service(service)
        progress_label.config(text=result)
        window.update()

    # قائمة المهام المجدولة لتعطيلها
    tasks_to_disable = [
        (r"\Microsoft\Windows\Customer Experience Improvement Program", "Consolidator"),
        (r"\Microsoft\Windows\Customer Experience Improvement Program", "KernelCeipTask"),
        (r"\Microsoft\Windows\Customer Experience Improvement Program", "UsbCeip"),
        (r"\Microsoft\Windows\DiskDiagnostic", "Microsoft-Windows-DiskDiagnosticDataCollector"),
        (r"\Microsoft\Windows\Shell", "FamilySafetyMonitor"),
        (r"\Microsoft\Windows\Shell", "FamilySafetyRefreshTask"),
        (r"\Microsoft\Windows\Windows Error Reporting", "QueueReporting"),
        (r"\Microsoft\Windows\Windows Error Reporting", "SR"),
        (r"\Microsoft\Windows\Windows Error Reporting", "UsbTracing"),
        (r"\Microsoft\Windows\RemoteAssistance", "RemoteAssistanceTask"),
        (r"\Microsoft\Windows\Media Center", "mcupdate"),
        (r"\Microsoft\Windows\Media Center", "mcupdate_scheduled"),
        (r"\Microsoft\Windows\Media Center", "MediaCenterRecoveryTask")
    ]

    # تعطيل المهام
    for task_path, task_name in tasks_to_disable:
        result = disable_scheduled_task(task_path, task_name)
        progress_label.config(text=result)
        window.update()

    # حذف الملفات المؤقتة
    delete_temp_files()

    end_time = time.time()  # تسجيل وقت انتهاء العملية
    elapsed_time = end_time - start_time  # حساب الوقت المستغرق
    progress_label.config(
        text=f"\nTotal time taken to complete all tasks: {elapsed_time:.2f} seconds \nYou must restart the device for the change to occur \n -AboArab-")

    # إضافة زر إعادة التشغيل وزر الإغلاق بعد انتهاء العملية
    restart_button = tk.Button(window, text="Restart PC Now", command=restart_computer, bg="red", fg="white")
    restart_button.pack(pady=10)

    restart_later_button = tk.Button(window, text="Restart Later", command=close_application, bg="green", fg="white")
    restart_later_button.pack(pady=10)

if __name__ == "__main__":
    # إعداد نافذة التطبيق
    window = tk.Tk()
    window.title("Task Progress")
    window.geometry("600x300")

    # إضافة عناصر واجهة المستخدم
    progress_label = tk.Label(window, text="Starting tasks...", wraplength=500)
    progress_label.pack(pady=20)

    # بدء تشغيل المهام
    start_time = time.time()  # تسجيل وقت بدء العملية
    run_tasks()

    # بدء الحلقة الرئيسية للواجهة الرسومية
    window.mainloop()
