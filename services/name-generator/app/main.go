package main

import (
	"fmt"
	"math/rand"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
	requestsTotal = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "http_requests_total",
			Help: "Total number of HTTP requests.",
		},
		[]string{"method", "handler", "code"},
	)
)

func init() {
	// Register custom metrics
	prometheus.MustRegister(requestsTotal)
}

func returnNameHandler(w http.ResponseWriter, r *http.Request) {
	// Create a new local random number generator with a seed
	rand := rand.New(rand.NewSource(time.Now().UnixNano()))

	// Generate a random integer between 0 and 5
	randomNumber := rand.Intn(5)

	names := []string{"Alice", "Bob", "Charlie", "Diana", "Mike", "Ray"}

	fmt.Fprintln(w, names[randomNumber])

	// Increment the metric
	requestsTotal.WithLabelValues(r.Method, "/", fmt.Sprintf("%d", 200)).Inc()
}

func main() {
	// register /metrics handler
	http.Handle("/metrics", promhttp.Handler())
	// register / handler
	http.HandleFunc("/", returnNameHandler)

	port := "0.0.0.0:8080"
	fmt.Printf("Starting server at http://localhost%s\n", port)
	err := http.ListenAndServe(port, nil)
	if err != nil {
		panic(err)
	}
}
