<template>
    <div class="admin-analiticas px-4 py-5">
        <div class="encabezado text-center mb-5">
            <h1 class="titulo">
                <i class="fas fa-chart-line me-2 text-white"></i>
                Analíticas de Productos
            </h1>
            <p class="subtitulo">Visualizá los productos más vistos, consultados y comprados.</p>
            <button @click="actualizarGraficos" class="btn-actualizar">
                <i class="fas fa-sync-alt me-1"></i> Actualizar datos
            </button>
        </div>



        <div class="graficos-stack">
            <div class="chart-box">
                <div class="chart-canvas">
                    <canvas id="chartVistos"></canvas>
                </div>
                <div class="chart-leyenda" id="leyenda-chartVistos">
                    <h4 class="leyenda-titulo">
                        <i class="fas fa-eye me-1 text-white"></i>
                        Más vistos
                    </h4>
                    <hr class="leyenda-separador" />
                </div>
            </div>

            <div class="chart-box">
                <div class="chart-canvas">
                    <canvas id="chartConsultas"></canvas>
                </div>
                <div class="chart-leyenda" id="leyenda-chartConsultas">
                    <h4 class="leyenda-titulo">
                        <i class="fas fa-mobile-alt me-1 text-white"></i>
                        Consultas por WhatsApp
                    </h4>
                    <hr class="leyenda-separador" />
                </div>
            </div>

            <div class="chart-box">
                <div class="chart-canvas">
                    <canvas id="chartCompras"></canvas>
                </div>
                <div class="chart-leyenda" id="leyenda-chartCompras">
                    <h4 class="leyenda-titulo">
                        <i class="fas fa-shopping-cart me-1 text-white"></i>
                        Compras
                    </h4>
                    <hr class="leyenda-separador" />
                </div>
            </div>
        </div>
    </div>

    <div v-if="!hayDatos" class="text-center text-white-50 mt-5">
        <i class="fas fa-chart-pie fa-2x mb-3"></i>
        <p>No hay suficientes datos para mostrar estadísticas aún.</p>
    </div>


    <SpinnerOverlay ref="refSpinner" mensaje="Obteniendo métricas..." />

</template>


<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import ChartDataLabels from 'chartjs-plugin-datalabels'
Chart.register(ChartDataLabels)
import axios from 'axios'
import SpinnerOverlay from '../components/SpinnerCarga.vue'

const refSpinner = ref(null)
const hayDatos = ref(false)

// 🎯 Reutilizamos en mounted y en botón
const actualizarGraficos = async () => {
    try {
        refSpinner.value?.mostrar()

        // 🧹 Eliminar gráficos previos si existen
        document.querySelectorAll('canvas').forEach(canvas => {
            const ctx = Chart.getChart(canvas)
            if (ctx) ctx.destroy()
        })

        const res = await axios.get('http://localhost:5000/api/products')
        const productos = res.data || []

        const topVistas = top(productos, 'vistas')
        const topConsultas = top(productos, 'consultas')
        const topCompras = top(productos, 'compras')

        hayDatos.value = topVistas.some(d => d.valor > 0) ||
            topConsultas.some(d => d.valor > 0) ||
            topCompras.some(d => d.valor > 0)

        const coloresV = generarColores(topVistas.length)
        const coloresC = generarColores(topConsultas.length)
        const coloresB = generarColores(topCompras.length)

        if (topVistas.some(d => d.valor > 0))
            crearGrafico('chartVistos', 'bar', 'Vistas',
                topVistas.map(d => d.nombre),
                topVistas.map(d => d.valor),
                coloresV, coloresV
            )

        if (topConsultas.some(d => d.valor > 0))
            crearGrafico('chartConsultas', 'doughnut', 'Consultas',
                topConsultas.map(d => d.nombre),
                topConsultas.map(d => d.valor),
                coloresC, coloresC
            )

        if (topCompras.some(d => d.valor > 0))
            crearGrafico('chartCompras', 'bar', 'Compras',
                topCompras.map(d => d.nombre),
                topCompras.map(d => d.valor),
                coloresB, coloresB,
                'horizontal'
            )

    } catch (error) {
        console.error('❌ Error al obtener métricas:', error)
    } finally {
        setTimeout(() => {
            refSpinner.value?.ocultar()
        }, 500)
    }
}

onMounted(() => {
    actualizarGraficos()
})

// 🧠 top por métrica
const top = (arr, key = 'nombre') =>
    arr
        .map(p => ({ nombre: p.nombre || 'Sin nombre', valor: Number(p[key] || 0) }))
        .sort((a, b) => b.valor - a.valor)
        .slice(0, 6)

// 📊 Crear gráfico
const crearGrafico = (
    id,
    tipo,
    label,
    labels,
    data,
    backgroundColor,
    borderColor,
    orientacion = 'vertical'
) => {
    new Chart(document.getElementById(id), {
        type: tipo,
        data: {
            labels,
            datasets: [{
                label,
                data,
                backgroundColor,
                borderColor,
                borderWidth: 1,
            }]
        },
        options: {
            indexAxis: tipo === 'bar' && orientacion === 'horizontal' ? 'y' : 'x',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.label}: ${ctx.raw}`
                    }
                },
                datalabels: tipo === 'doughnut' ? {
                    color: '#fff',
                    font: { weight: 'bold', size: 14 },
                    formatter: value => value > 0 ? value : ''
                } : false
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            },
            scales: tipo === 'bar' ? {
                x: orientacion === 'horizontal'
                    ? {
                        beginAtZero: true,
                        ticks: { color: '#ccc' }
                    }
                    : {
                        ticks: {
                            color: '#ccc',
                            callback: function (value) {
                                const label = this.getLabelForValue(value)
                                return label.length > 20 ? label.slice(0, 18) + '…' : label
                            }
                        }
                    },
                y: orientacion === 'horizontal'
                    ? {
                        ticks: {
                            color: '#ccc',
                            callback: function (value) {
                                const label = this.getLabelForValue(value)
                                return label.length > 20 ? label.slice(0, 18) + '…' : label
                            }
                        }
                    }
                    : {
                        beginAtZero: true,
                        ticks: { color: '#ccc' }
                    }
            } : {}
        },
        plugins: tipo === 'doughnut' ? [ChartDataLabels] : []
    })

    // 📌 Agregar leyenda dinámica
    const leyendaContainer = document.getElementById(`leyenda-${id}`)
    if (leyendaContainer) {
        const itemsExistentes = leyendaContainer.querySelectorAll('.leyenda-item')
        itemsExistentes.forEach(item => item.remove())

        labels.forEach((nombre, i) => {
            const color = backgroundColor[i]
            const item = document.createElement('div')
            item.className = 'leyenda-item'
            item.innerHTML = `
        <div class="color-box" style="background-color: ${color}"></div>
        <span title="${nombre}">${nombre.length > 35 ? nombre.slice(0, 32) + '…' : nombre}</span>
      `
            leyendaContainer.appendChild(item)
        })
    }
}

// 🎨 Paleta de colores pro + fallback
function generarColores(cantidad) {
    const baseColors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#66FF66', '#FF66CC',
        '#00CED1', '#D2691E', '#C71585', '#87CEEB'
    ]

    const colores = cantidad <= baseColors.length
        ? baseColors.slice(0, cantidad)
        : [...baseColors, ...Array.from({ length: cantidad - baseColors.length }, (_, i) =>
            `hsl(${(i * 137.5) % 360}, 70%, 55%)`
        )]

    return colores.sort(() => Math.random() - 0.5)
}
</script>





<style scoped>
.admin-analiticas {
    min-height: 100vh;
    background-color: #121212;
    color: white;
}

.encabezado .titulo {
    font-size: 2.8rem;
    font-weight: bold;
    color: #ffd700;
    margin-bottom: 0.5rem;
}

.encabezado .subtitulo {
    color: #ccc;
    font-size: 1.2rem;
}

/* Gráficos uno abajo del otro, bien espaciosos */
.graficos-stack {
    display: flex;
    flex-direction: column;
    gap: 3rem;
}

/* Cada caja de gráfico ocupa toda la fila */
.chart-box {
    display: grid;
    grid-template-columns: 60% 40%;
    background-color: #1e1e1e;
    border-radius: 20px;
    padding: 3rem;
    gap: 2rem;
    align-items: center;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    transition: transform 0.3s ease;
}

.chart-box:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
}

.chart-canvas {
    display: flex;
    justify-content: center;
    align-items: center;
    max-height: 400px;
}

.chart-box canvas {
    width: 100% !important;
    height: auto !important;
    max-height: 350px;
}

.chart-leyenda {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    font-size: 1rem;
    color: #eee;
    justify-content: center;
    max-height: 350px;
    overflow-y: auto;
    padding-left: 1rem;
    border-left: 2px solid #2c2c2c;
}

.leyenda-titulo {
    font-size: 1.1rem;
    color: #ffd700;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.leyenda-separador {
    border: none;
    height: 1px;
    background-color: #333;
    margin: 0 0 0.5rem 0;
}

.leyenda-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    line-height: 1.4;
}

.leyenda-item:hover {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 6px;
    padding: 2px 6px;
    cursor: default;
}


.color-box {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    flex-shrink: 0;
    animation: aparecerGrafico 0.5s ease;
}

@keyframes aparecerGrafico {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.btn-actualizar {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background-color: transparent;
    border: 2px solid #ffc107;
    color: #ffc107;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-family: inherit;
    font-size: 1rem;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

.btn-actualizar::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background-color: #ffc107;
    z-index: -1;
    transition: all 0.4s ease;
}

.btn-actualizar:hover::before {
    left: 0;
}

.btn-actualizar:hover {
    color: #121212;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 193, 7, 0.3);
}


@media (max-width: 992px) {
    .chart-box {
        grid-template-columns: 1fr;
        padding: 2rem 1.5rem;
    }

    .chart-canvas {
        max-height: 340px;
    }

    .chart-leyenda {
        border-left: none;
        border-top: 1px solid #2c2c2c;
        padding-left: 0;
        padding-top: 1.5rem;
    }
}

@media (max-width: 768px) {
    .encabezado .titulo {
        font-size: 2.2rem;
        text-align: center;
    }

    .encabezado .subtitulo {
        font-size: 1rem;
        text-align: center;
    }

    .chart-box {
        padding: 1.5rem 1rem;
        gap: 1.5rem;
    }

    .chart-canvas {
        min-height: 280px;
    }

    .leyenda-titulo {
        font-size: 1rem;
        text-align: center;
    }

    .leyenda-item {
        justify-content: center;
        text-align: center;
    }
}

@media (max-width: 480px) {
    .chart-box {
        padding: 1rem;
        gap: 1rem;
    }

    .chart-canvas {
        min-height: 260px;
    }

    .chart-box canvas {
        height: 100% !important;
    }

    .leyenda-item span {
        font-size: 0.9rem;
    }

    .color-box {
        width: 14px;
        height: 14px;
    }
}

@media (max-width: 380px) {
    .leyenda-item span {
        font-size: 0.8rem;
    }

    .leyenda-item {
        gap: 0.3rem;
    }
}
</style>
