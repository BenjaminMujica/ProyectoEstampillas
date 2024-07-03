import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencias instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print("Error durante la instalación de dependencias:", e)
    except Exception as e:
        print("Ocurrió un error:", e)

if __name__ == "__main__":
    install_requirements()
