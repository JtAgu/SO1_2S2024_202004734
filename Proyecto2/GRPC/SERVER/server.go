package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// Definir la estructura para el JSON esperado
type Student struct {
	Student    string `json:"student"`
	Age        int    `json:"age"`
	Faculty    string `json:"faculty"`
	Discipline int    `json:"discipline"`
}

// Manejar la solicitud POST
func studentHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	var student Student
	err := json.NewDecoder(r.Body).Decode(&student)
	if err != nil {
		http.Error(w, "Failed to decode JSON", http.StatusBadRequest)
		return
	}

	// Imprimir la información recibida
	fmt.Printf("Received: %+v\n", student)

	// Enviar respuesta
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Student information received"))
}

func main() {
	http.HandleFunc("/students", studentHandler)
	fmt.Println("Server is running on port 8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Failed to start server:", err)
	}
}
