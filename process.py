import subprocess
from datetime import datetime

current_datetime = datetime.today().strftime('%d-%m-%Y-%H:%M')
report_filename = f"{current_datetime}-scan.txt"

process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
output, error = process.communicate()

if error:
    print(f"Ошибка выполнения команды: {error}")
    exit(1)

processes = output.decode('utf-8').split('\n')[1:-1]
user_processes = {}
total_memory = 0
total_cpu = 0
max_memory_process = ('', 0)
max_cpu_process = ('', 0)

for process_info in processes:
    process_data = process_info.split()
    username = process_data[0]
    memory = float(process_data[3])
    cpu = float(process_data[2])

    if username in user_processes:
        user_processes[username] += 1
    else:
        user_processes[username] = 1

    total_memory += memory
    total_cpu += cpu

    if memory > max_memory_process[1]:
        max_memory_process = (process_data[10][:20], memory)

    if cpu > max_cpu_process[1]:
        max_cpu_process = (process_data[10][:20], cpu)

print("Отчёт о состоянии системы:\n")
print(f"Пользователи системы: {', '.join(user_processes.keys())}\n")
print(f"Процессов запущено: {len(processes)}\n")
print("Пользовательских процессов:\n")
for user, count in user_processes.items():
    print(f"{user}: {count}\n")
print("...\n")
print(f"Всего памяти используется: {total_memory:.1f}%\n")
print(f"Всего CPU используется: {total_cpu:.1f}%\n")
print(f"Больше всего памяти использует: ({max_memory_process[1]:.1f}%) {max_memory_process[0]}\n")
print(f"Больше всего CPU использует: ({max_cpu_process[1]:.1f}%) {max_cpu_process[0]}\n")
print("Отчёт сохранён в файле:", report_filename)

with open(report_filename, 'w') as report_file:
    report_file.write("Отчёт о состоянии системы:\n")
    report_file.write(f"Пользователи системы: {', '.join(user_processes.keys())}\n")
    report_file.write(f"Процессов запущено: {len(processes)}\n")
    report_file.write("Пользовательских процессов:\n")
    for user, count in user_processes.items():
        report_file.write(f"{user}: {count}\n")
    report_file.write("...\n")
    report_file.write(f"Всего памяти используется: {total_memory:.1f}%\n")
    report_file.write(f"Всего CPU используется: {total_cpu:.1f}%\n")
    report_file.write(f"Больше всего памяти использует: ({max_memory_process[1]:.1f}%) {max_memory_process[0]}\n")
    report_file.write(f"Больше всего CPU использует: ({max_cpu_process[1]:.1f}%) {max_cpu_process[0]}\n")