#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/proc_fs.h> // trae las funciones para crear archivos en /proc
#include <linux/seq_file.h> // trae las funciones para escribir en archivos en /proc
#include <linux/mm.h> // trae las funciones para manejar la memoria
#include <linux/sched.h> // trae las funciones para manejar los procesos
#include <linux/timer.h> // trae las funciones para manejar los timers
#include <linux/jiffies.h> // trae las funciones para manejar los jiffies, que son los ticks del sistema
#include <linux/sched/signal.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Justin Aguirre");
MODULE_DESCRIPTION("Modulo para leer informacion de memoria y CPU");


#define PROC_NAME "sysinfo_202004734" // nombre del archivo en /proc

/* 
    Esta función se encarga de obtener la información de la memoria
    - si_meminfo: recibe un puntero a una estructura sysinfo, la cual se llena con la información de la memoria
*/
static int sysinfo_show(struct seq_file *m, void *v) {
    struct sysinfo si; // estructura que contiene la informacion de la memoria
    struct task_struct *task;
    si_meminfo(&si); // obtiene la informacion de la memoria
    
    /*  
        El seq_printf se encarga de escribir en el archivo en /proc
        - m: es el archivo en /pro
    */

    seq_printf(m, "Total RAM: %lu KB\n", si.totalram * 4);
    seq_printf(m, "Free RAM: %lu KB\n", si.freeram * 4);
    seq_printf(m, "Shared RAM: %lu KB\n", si.sharedram * 4);
    seq_printf(m, "Buffer RAM: %lu KB\n", si.bufferram * 4);
    seq_printf(m, "Total Swap: %lu KB\n", si.totalswap * 4);
    seq_printf(m, "Free Swap: %lu KB\n", si.freeswap * 4);

    seq_printf(m, "Number of processes: %d\n", num_online_cpus());

    for_each_process(task){
        if(task->parent){
            printk(KERN_INFO "Parent Process: %s [PID: %d]\n",task->parent->comm, task->parent->pid);
            printk(KERN_INFO "Child Process: %s [PID: %d]\n",task->comm, task->pid);
        }
    }

    return 0;
};

/* 
    Esta función se ejecuta cuando se abre el archivo en /proc
    - single_open: se encarga de abrir el archivo y ejecutar la función sysinfo_show
*/
static int sysinfo_open(struct inode *inode, struct file *file) {
    return single_open(file, sysinfo_show, NULL);
}

/* 
    Esta estructura contiene las operaciones a realizar cuando se accede al archivo en /proc
    - proc_open: se ejecuta cuando se abre el archivo
    - proc_read: se ejecuta cuando se lee el archivo
*/

static const struct proc_ops sysinfo_ops = {
    .proc_open = sysinfo_open,
    .proc_read = seq_read,
};


/* 
    Esta macro se encarga de hacer dos cosas:
    1. Ejecutar la función proc_create, la cual recibe el nombre del archivo a guardar en /proc, permisos,
        y la estructura con las operaciones a realizar

    2. Imprimir un mensaje en el log del kernel
*/
static int __init sysinfo_init(void) {
    proc_create(PROC_NAME, 0, NULL, &sysinfo_ops);
    printk(KERN_INFO "sysinfo_202004734 module loaded\n");
    return 0;
}

/* 
    Esta macro se encarga de hacer dos cosas:
    1. Ejecutar la función remove_proc_entry, la cual recibe el nombre del archivo a eliminar de /proc
*/
static void __exit sysinfo_exit(void) {
    remove_proc_entry(PROC_NAME, NULL);
    printk(KERN_INFO "sysinfo_202004734 module unloaded\n");
}

module_init(sysinfo_init);
module_exit(sysinfo_exit);