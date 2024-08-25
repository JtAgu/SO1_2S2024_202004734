#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/mm.h>
#include <linux/sched.h>
#include <linux/sched/signal.h>
#include <linux/jiffies.h>
#include <linux/uaccess.h>
#include <linux/fs.h>
#include <linux/ctype.h>
#include <linux/slab.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Justin Aguirre");
MODULE_DESCRIPTION("Modulo para leer informacion de memoria y CPU");

// Definición del nombre del archivo en /proc
#define PROC_NAME "sysinfo_20200734"

// Función para calcular el porcentaje de uso de memoria
static unsigned long calculate_memory_usage(unsigned long total, unsigned long free) {
    return total - free;
}

// Función para mostrar la información en el archivo /proc
static int sysinfo_show(struct seq_file *m, void *v) {
    struct sysinfo si;
    struct task_struct *task;
    unsigned long totalram, freeram, usedram;
    unsigned long pagesize = 4096; // Tamaño de una página en bytes (puede variar según la arquitectura)

    si_meminfo(&si);

    totalram = si.totalram * (pagesize / 1024);
    freeram = si.freeram * (pagesize / 1024);
    usedram = calculate_memory_usage(totalram, freeram);

    seq_printf(m, "Total RAM: %lu KB\n", totalram);
    seq_printf(m, "Free RAM: %lu KB\n", freeram);
    seq_printf(m, "Used RAM: %lu KB\n", usedram);

    seq_printf(m, "\nProcesses related to containers:\n");

    for_each_process(task) {
        if (task->mm) {
            // Obtener el comando de línea
            char comm[TASK_COMM_LEN];
            get_task_comm(comm, task);

            // Obtener información de memoria
            unsigned long vsz = task->mm->total_vm * (pagesize / 1024); // Memoria virtual en KB
            unsigned long rss = get_mm_rss(task->mm) * (pagesize / 1024); // Memoria física en KB

            // Calcula el porcentaje de memoria utilizada
            unsigned long mem_total = totalram; // Total RAM
            unsigned long mem_used = usedram; // RAM en uso
            unsigned long mem_usage_pct = (rss * 100) / mem_total;

            // Calcula el porcentaje de CPU utilizado
            unsigned long cpu_usage_pct = (task->se.sum_exec_runtime * 100) / (jiffies_to_msecs(jiffies) * 1000);

            seq_printf(m, "PID: %d\n", task->pid);
            seq_printf(m, "Name: %s\n", comm);
            seq_printf(m, "Command Line: %s\n", task->comm);
            seq_printf(m, "VSZ: %lu KB\n", vsz);
            seq_printf(m, "RSS: %lu KB\n", rss);
            seq_printf(m, "Memory Usage: %lu%%\n", mem_usage_pct);
            seq_printf(m, "CPU Usage: %lu%%\n\n", cpu_usage_pct);
        }
    }

    return 0;
}

// Función para abrir el archivo /proc
static int sysinfo_open(struct inode *inode, struct file *file) {
    return single_open(file, sysinfo_show, NULL);
}

// Operaciones del archivo /proc
static const struct proc_ops sysinfo_ops = {
    .proc_open = sysinfo_open,
    .proc_read = seq_read,
};

// Inicialización del módulo
static int __init sysinfo_init(void) {
    proc_create(PROC_NAME, 0, NULL, &sysinfo_ops);
    printk(KERN_INFO "sysinfo_20200734 module loaded\n");
    return 0;
}

// Salida del módulo
static void __exit sysinfo_exit(void) {
    remove_proc_entry(PROC_NAME, NULL);
    printk(KERN_INFO "sysinfo_20200734 module unloaded\n");
}

module_init(sysinfo_init);
module_exit(sysinfo_exit);