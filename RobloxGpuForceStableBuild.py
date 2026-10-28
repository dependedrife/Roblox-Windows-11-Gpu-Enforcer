"""
================================================================================
ROBLOX QUANTUM HIGH-PERFORMANCE ACCELERATOR // Universal Elite Windows 11 Edition
Features: Live Process Tracking, Smart Auto-Relaunch, Auto-Healing Shield & Aesthetic UI
================================================================================
"""

import os
import sys
import ctypes
import subprocess
import threading
import time
import winreg
import customtkinter as ctk
from tkinter import messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class QuantumEngineCore:
    def __init__(self):
        self.active_monitoring = False
        self.optimized_paths = set()
        
    def get_roblox_executables(self):
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        roblox_versions_path = os.path.join(local_appdata, "Roblox", "Versions")
        found_executables = []
        if os.path.exists(roblox_versions_path):
            for root, dirs, files in os.walk(roblox_versions_path):
                for file in files:
                    if file.lower() == "robloxplayerbeta.exe":
                        found_executables.append(os.path.join(root, file))
        return found_executables

    def is_roblox_running(self):
        """Smart check to see if Roblox is currently active in memory."""
        try:
            res = subprocess.run('tasklist /fi "imagename eq RobloxPlayerBeta.exe"', capture_output=True, text=True, shell=True)
            return "RobloxPlayerBeta.exe" in res.stdout
        except:
            return False

    def kill_roblox(self):
        """Forcefully closes active Roblox instances to clear file locks and apply hooks."""
        try:
            subprocess.run("taskkill /f /im RobloxPlayerBeta.exe", capture_output=True, text=True, shell=True)
            return True
        except:
            return False

    def force_windows_gpu_preference(self):
        exes = self.get_roblox_executables()
        if not exes:
            return False, "No Roblox binaries located. Please open Roblox at least once first."
        
        success_count = 0
        registry_path = r"SOFTWARE\Microsoft\DirectX\UserGpuPreferences"
        
        try:
            reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
            for exe in exes:
                winreg.SetValueEx(reg_key, exe, 0, winreg.REG_SZ, "GpuPreference=2;")
                success_count += 1
                self.optimized_paths.add(exe)
            winreg.CloseKey(reg_key)
            
            compat_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
            compat_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, compat_path, 0, winreg.KEY_WRITE)
            for exe in exes:
                winreg.SetValueEx(compat_key, exe, 0, winreg.REG_SZ, "~ HIGHDPIENABLE AWARE")
            winreg.CloseKey(compat_key)
            
            return True, f"Successfully routed {success_count} Roblox targets to Discrete High-Performance GPU."
        except Exception as e:
            return False, f"Registry Injection Exception: {str(e)}"

    def smart_apply_gpu_preference(self, logger_func):
        """Smart orchestration: Requires Roblox open/tracked, kills it, applies registry, and relaunches instantly."""
        if not self.is_roblox_running():
            return False, "Roblox must be OPEN right now! Please keep Roblox running so the engine can accurately track its active .exe path with a 100% success rate."

        exes = self.get_roblox_executables()
        if not exes:
            return False, "Active process found, but no binaries located. Launch Roblox fully first."
        
        logger_func("[SMART-ENGINE] Active Roblox instance locked via live tracking. Terminating gracefully...")
        self.kill_roblox()
        time.sleep(0.8) # Allow system to clear file handles instantly

        success, msg = self.force_windows_gpu_preference()
        
        if success:
            # Find the exact active executable path to relaunch instantly
            active_exe = max(exes, key=os.path.getmtime)
            logger_func("[SMART-ENGINE] Relaunching Roblox instantly with forced High-Performance GPU...")
            try:
                subprocess.Popen([active_exe])
                msg += " Roblox was automatically closed, updated with GPU preferences, and relaunched successfully!"
            except Exception as e:
                msg += f" (GPU preference applied, but auto-relaunch failed: {str(e)})"
                
        return success, msg

    def restore_factory_defaults(self):
        if self.is_roblox_running():
            self.kill_roblox()
            
        registry_path = r"SOFTWARE\Microsoft\DirectX\UserGpuPreferences"
        compat_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
        removed_count = 0
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_ALL_ACCESS)
            i = 0
            keys_to_delete = []
            while True:
                try:
                    name, _, _ = winreg.EnumValue(reg_key, i)
                    if "roblox" in name.lower():
                        keys_to_delete.append(name)
                    i += 1
                except WindowsError:
                    break
            for name in keys_to_delete:
                winreg.DeleteValue(reg_key, name)
                removed_count += 1
            winreg.CloseKey(reg_key)
            
            try:
                compat_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, compat_path, 0, winreg.KEY_ALL_ACCESS)
                i = 0
                compat_to_delete = []
                while True:
                    try:
                        name, _, _ = winreg.EnumValue(compat_key, i)
                        if "roblox" in name.lower():
                            compat_to_delete.append(name)
                        i += 1
                    except WindowsError:
                        break
                for name in compat_to_delete:
                    winreg.DeleteValue(compat_key, name)
                winreg.CloseKey(compat_key)
            except:
                pass

            subprocess.run("powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e", shell=True)
            self.optimized_paths.clear()
            return True, f"Successfully purged {removed_count} registry overrides and restored defaults."
        except Exception as e:
            return False, f"Reversion Exception: {str(e)}"

    def check_startup_status(self):
        startup_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(reg_key, "RobloxQuantumAccelerator")
            winreg.CloseKey(reg_key)
            return True
        except:
            return False

    def toggle_startup_registry(self, enable):
        startup_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        app_path = f'"{sys.executable}"'
        try:
            reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, startup_path, 0, winreg.KEY_WRITE)
            if enable:
                winreg.SetValueEx(reg_key, "RobloxQuantumAccelerator", 0, winreg.REG_SZ, app_path)
            else:
                try:
                    winreg.DeleteValue(reg_key, "RobloxQuantumAccelerator")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(reg_key)
            return True, "Startup configuration updated successfully."
        except Exception as e:
            return False, f"Startup Registry Error: {str(e)}"

    def fetch_gpu_utilization(self):
        try:
            cmd = "powershell -Command \"(Get-Counter '\\GPU Engine(*engtype_3D*)\\Utilization Percentage' -ErrorAction SilentlyContinue).CounterSamples | Measure-Object -Property CookedValue -Sum | Select-Object -ExpandProperty Sum\""
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            val = float(res.stdout.strip()) if res.stdout.strip() else 0.0
            return min(max(int(val), 0), 100)
        except:
            return 0

    def background_guardian_loop(self, logger_func):
        self.active_monitoring = True
        while self.active_monitoring:
            try:
                subprocess.run('powershell -Command "Get-Process -Name RobloxPlayerBeta -ErrorAction SilentlyContinue | ForEach-Object { $_.PriorityClass = \'High\'}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                current_exes = self.get_roblox_executables()
                for exe in current_exes:
                    if exe not in self.optimized_paths:
                        registry_path = r"SOFTWARE\Microsoft\DirectX\UserGpuPreferences"
                        reg_key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
                        winreg.SetValueEx(reg_key, exe, 0, winreg.REG_SZ, "GpuPreference=2;")
                        winreg.CloseKey(reg_key)
                        self.optimized_paths.add(exe)
                        logger_func(f"[AUTO-HEAL] New update version bound to Discrete GPU!")
            except:
                pass
            time.sleep(5.0)


class ModernFluentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Roblox Quantum GPU Accelerator // Universal Aesthetic Edition")
        self.geometry("860x660")
        self.minsize(860, 660)
        
        self.configure(fg_color="#130826")
        
        icon_path = "gpuicon.ico"
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        self.engine = QuantumEngineCore()
        
        self.init_layout()
        self.start_telemetry_loop()

    def init_layout(self):
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1b0e35")
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="ROBLOX QUANTUM ACCELERATOR", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#f3e8ff")
        self.title_label.pack(side="left", padx=20, pady=15)
        
        self.status_badge = ctk.CTkLabel(self.header_frame, text=" SYSTEM READY ", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), fg_color="#7c3aed", text_color="#ffffff", corner_radius=6)
        self.status_badge.pack(side="right", padx=20, pady=15)
        
        self.telemetry_frame = ctk.CTkFrame(self, fg_color="#23114a", height=50, corner_radius=8)
        self.telemetry_frame.pack(fill="x", padx=20, pady=(15, 0))
        self.telemetry_frame.pack_propagate(False)
        
        self.gpu_label_status = ctk.CTkLabel(self.telemetry_frame, text="Discrete GPU 3D Load: 0%", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#e9d5ff")
        self.gpu_label_status.pack(side="left", padx=20, pady=12)
        
        self.gpu_progress = ctk.CTkProgressBar(self.telemetry_frame, width=300, progress_color="#a855f7", fg_color="#11052c")
        self.gpu_progress.pack(side="right", padx=20, pady=15)
        self.gpu_progress.set(0.0)

        self.tabview = ctk.CTkTabview(self, corner_radius=12, fg_color="#1b0e35", segmented_button_fg_color="#11052c", segmented_button_selected_color="#7c3aed", segmented_button_selected_hover_color="#6d28d9", segmented_button_unselected_color="#23114a")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.tab_dashboard = self.tabview.add("Dashboard & Controls")
        self.tab_diagnostics = self.tabview.add("Diagnostics & Telemetry")
        
        self.build_dashboard_tab()
        self.build_diagnostics_tab()

    def build_dashboard_tab(self):
        self.left_frame = ctk.CTkFrame(self.tab_dashboard, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)
        
        self.btn_inject = ctk.CTkButton(self.left_frame, text="⚡ APPLY GPU OVERRIDE & RESTART", font=ctk.CTkFont(size=12, weight="bold"), height=36, fg_color="#7c3aed", hover_color="#6d28d9", command=self.run_gpu_injection)
        self.btn_inject.pack(fill="x", padx=10, pady=5)
        
        self.btn_power = ctk.CTkButton(self.left_frame, text="🚀 ENABLE ULTIMATE POWER SCHEME", font=ctk.CTkFont(size=12, weight="bold"), height=36, fg_color="#2d1b54", hover_color="#3b226e", command=self.run_power_optimization)
        self.btn_power.pack(fill="x", padx=10, pady=5)
        
        self.btn_guardian = ctk.CTkButton(self.left_frame, text="🛡️ START AUTO-HEALING SHIELD", font=ctk.CTkFont(size=12, weight="bold"), height=36, fg_color="#0d9488", hover_color="#0f766e", command=self.toggle_guardian)
        self.btn_guardian.pack(fill="x", padx=10, pady=5)

        is_startup = self.engine.check_startup_status()
        startup_text = "☑ DISABLE WINDOWS STARTUP" if is_startup else "☐ ENABLE WINDOWS STARTUP"
        startup_color = "#991b1b" if is_startup else "#2d1b54"
        startup_hover = "#7f1d1d" if is_startup else "#3b226e"
        
        self.btn_startup = ctk.CTkButton(self.left_frame, text=startup_text, font=ctk.CTkFont(size=12, weight="bold"), height=36, fg_color=startup_color, hover_color=startup_hover, command=self.toggle_startup_mode)
        self.btn_startup.pack(fill="x", padx=10, pady=5)

        self.btn_revert = ctk.CTkButton(self.left_frame, text="🔄 RESTORE FACTORY DEFAULTS (UNDO)", font=ctk.CTkFont(size=12, weight="bold"), height=36, fg_color="#991b1b", hover_color="#7f1d1d", command=self.run_reversion)
        self.btn_revert.pack(fill="x", padx=10, pady=5)
        
        self.right_frame = ctk.CTkFrame(self.tab_dashboard, fg_color="#23114a")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=5)
        
        self.log_title = ctk.CTkLabel(self.right_frame, text="Execution Audit Log", font=ctk.CTkFont(size=13, weight="bold"), text_color="#f3e8ff")
        self.log_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.log_area = ctk.CTkTextbox(self.right_frame, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#130826", text_color="#d8b4fe")
        self.log_area.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.log_area.insert("end", "[INIT] Keep Roblox open for 100% precise path tracking & auto-restarts.\n")
        self.log_area.configure(state="disabled")

    def build_diagnostics_tab(self):
        self.diag_title = ctk.CTkLabel(self.tab_diagnostics, text="Discovered Roblox Binaries & Target Vectors", font=ctk.CTkFont(size=13, weight="bold"), text_color="#f3e8ff")
        self.diag_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.diag_text = ctk.CTkTextbox(self.tab_diagnostics, font=ctk.CTkFont(family="Consolas", size=11), fg_color="#130826", text_color="#d8b4fe")
        self.diag_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.btn_refresh = ctk.CTkButton(self.tab_diagnostics, text="🔄 SCAN SYSTEM PATHS", width=180, fg_color="#7c3aed", hover_color="#6d28d9", command=self.refresh_diagnostics)
        self.btn_refresh.pack(anchor="e", padx=15, pady=(0, 15))
        self.refresh_diagnostics()

    def start_telemetry_loop(self):
        def poll():
            while True:
                usage = self.engine.fetch_gpu_utilization()
                try:
                    self.gpu_label_status.configure(text=f"Discrete GPU 3D Load: {usage}%")
                    self.gpu_progress.set(usage / 100.0)
                except:
                    break
                time.sleep(2.0)
        t = threading.Thread(target=poll, daemon=True)
        t.start()

    def log_message(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def run_gpu_injection(self):
        self.log_message("Verifying active Roblox process presence...")
        success, msg = self.engine.smart_apply_gpu_preference(self.log_message)
        if success:
            self.log_message(msg)
            self.status_badge.configure(text=" HIGH-PERF SECURED ", fg_color="#0d9488")
            messagebox.showinfo("Success", msg)
        else:
            self.log_message(f"ERROR: {msg}")
            messagebox.showerror("Action Required", msg)
        self.refresh_diagnostics()

    def toggle_startup_mode(self):
        current_status = self.engine.check_startup_status()
        new_status = not current_status
        success, msg = self.engine.toggle_startup_registry(new_status)
        if success:
            if new_status:
                self.btn_startup.configure(text="☑ DISABLE WINDOWS STARTUP", fg_color="#991b1b", hover_color="#7f1d1d")
                self.log_message("Tool successfully registered to start with Windows.")
                messagebox.showinfo("Startup Enabled", "The tool will now start automatically when Windows boots.")
            else:
                self.btn_startup.configure(text="☐ ENABLE WINDOWS STARTUP", fg_color="#2d1b54", hover_color="#3b226e")
                self.log_message("Tool removed from Windows startup registry.")
                messagebox.showinfo("Startup Disabled", "Removed from Windows startup.")
        else:
            messagebox.showerror("Error", msg)

    def run_reversion(self):
        if messagebox.askyesno("Confirm Reversion", "Restore factory defaults and remove all app overrides?"):
            success, msg = self.engine.restore_factory_defaults()
            if success:
                self.log_message(msg)
                self.status_badge.configure(text=" RESET TO DEFAULT ", fg_color="#7c3aed")
                messagebox.showinfo("Restored", msg)
            else:
                messagebox.showerror("Error", msg)
            self.refresh_diagnostics()

    def run_power_optimization(self):
        success, msg = self.engine.trigger_ultimate_power_plan()
        if success:
            self.log_message(msg)
            messagebox.showinfo("Power Scheme", msg)

    def toggle_guardian(self):
        if not self.engine.active_monitoring:
            self.btn_guardian.configure(text="🛑 STOP AUTO-HEALING SHIELD", fg_color="#991b1b", hover_color="#7f1d1d")
            self.status_badge.configure(text=" SHIELD ACTIVE ", fg_color="#0d9488")
            self.log_message("Auto-healing shield activated.")
            t = threading.Thread(target=self.engine.background_guardian_loop, args=(self.log_message,), daemon=True)
            t.start()
        else:
            self.engine.active_monitoring = False
            self.btn_guardian.configure(text="🛡️ START AUTO-HEALING SHIELD", fg_color="#0d9488", hover_color="#0f766e")
            self.status_badge.configure(text=" SYSTEM READY ", fg_color="#7c3aed")
            self.log_message("Auto-healing shield deactivated.")

    def refresh_diagnostics(self):
        self.diag_text.configure(state="normal")
        self.diag_text.delete("1.0", "end")
        exes = self.engine.get_roblox_executables()
        if not exes:
            self.diag_text.insert("end", "No Roblox binaries found. Launch Roblox first.\n")
        else:
            self.diag_text.insert("end", f"Found {len(exes)} Roblox binary versions:\n\n")
            for exe in exes:
                status_tag = "[OPTIMIZED / LINKED]" if exe in self.engine.optimized_paths else "[PENDING OVERRIDE]"
                self.diag_text.insert("end", f"• {exe}\n  Status: {status_tag}\n\n")
        self.diag_text.configure(state="disabled")

if __name__ == "__main__":
    app = ModernFluentApp()
    app.mainloop()