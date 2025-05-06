import subprocess
import argparse
from typing import List

def clean_arg_list(text: str) -> List:
    try:
        aux = text.replace('[', '')
        aux = aux.replace(']', '')
        aux = aux.replace('{', '')
        aux = aux.replace('}', '')
        list_processes = list(map(int, aux.split(',')))
        return list_processes
    except Exception as ex:
        print("No se pudo obtener la lista de procesos")
        print(ex)
        return []

def main():
    try:
        parser = argparse.ArgumentParser(description="Ejecuta un script paralelizado")
        parser.add_argument('--filename', type=str, help='Nombre del archivo python a ejecutar (ejemplo.py)')
        parser.add_argument('--processes', type=str, help='Lista de procesos a ejecutar en loop ([1, 2, 3])')
        parser.add_argument('--cities', type=int, help='Número de ciudades')

        args = parser.parse_args()

        target_script = args.filename
        list_processes = clean_arg_list(args.processes)
        cities = args.cities

        print(f"Ejecutando el script: {target_script}")
        print(f"Rango de Procesos: {list_processes}")
        print(f"Cantidad de Ciudades: {cities}")

        if len(list_processes) <= 0:
            raise Exception('Debe enviar por lo menos 1 proceso')
        if not cities:
            raise Exception('Debe especificar el número de ciudades')

        for num_procs in list_processes:
            print(f"\n🔁 Ejecutando con {num_procs} procesos...\n")
            command = [
                "mpiexec",
                "-n", str(num_procs),
                "python",
                target_script,
                str(cities)
            ]
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error al ejecutar mpiexec con {num_procs} procesos:")
                print(e)
    except Exception as ex:
        print("Ocurrió un error")
        print(ex)

if __name__ == "__main__":
    main()
