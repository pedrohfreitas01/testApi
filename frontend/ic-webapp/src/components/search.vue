<template>
  <div class="container">
    <h2>Buscar Operadoras</h2>
    <div class="search-box">
      <!-- buscar o TERMO -->
      <input
        v-model="termoBusca"
        placeholder="Digite um termo..."
        @keyup.enter="buscarDados"
      />
      <!-- load de carregamento se tiver -->
      <button @click="buscarDados" :disabled="carregando">
        {{ carregando ? "Buscando..." : "Buscar" }}
      </button>
    </div>

    <!-- status -->
    <div v-if="carregando" class="status loading">Carregando...</div>
    <div v-if="erro" class="status error">{{ erro }}</div>

    <!-- resultados -->
    <div v-if="todosResultados.length > 0" class="results-container">
      <div class="results-header">
        <h3>Total de resultados: {{ todosResultados.length }}</h3>
        <div class="pagination-controls">
          <button @click="paginaAnterior" :disabled="paginaAtual === 1">
            Anterior
          </button>
          <span>Página {{ paginaAtual }} de {{ totalPaginas }}</span>
          <button @click="proximaPagina" :disabled="paginaAtual === totalPaginas">
            Próxima
          </button>
        </div>
      </div>

      <!-- card dos Operadores pegando a API -->
      <div class="results-list">
        <div
          v-for="(operadora, index) in resultadosPaginados"
          :key="index"
          class="operadora-card"
        >
          <div class="operadora-info">
            <h4>{{ formatarCampo(operadora.Razao_Social) }}</h4>
            <div class="operadora-details">
              <div><strong>Cidade:</strong> {{ operadora.Cidade || "Não disponível" }}</div>
              <div><strong>CNPJ:</strong> {{ formatarCampo(operadora.CNPJ) }}</div>
              <div><strong>Telefone:</strong> {{ formatarCampo(operadora.Telefone) }}</div>
              <div><strong>UF:</strong> {{ formatarCampo(operadora.UF) }}</div>
              <div v-if="operadora.Nome_Fantasia">
                <strong>Nome Fantasia:</strong> {{ formatarCampo(operadora.Nome_Fantasia) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      termoBusca: "",
      todosResultados: [],
      erro: "",
      carregando: false,
      paginaAtual: 1,
      itensPorPagina: 20,
    };
  },
  computed: {
    resultadosPaginados() {
      // paginacao 
      const inicio = (this.paginaAtual - 1) * this.itensPorPagina;
      return this.todosResultados.slice(inicio, inicio + this.itensPorPagina);
    },
    totalPaginas() {
      return Math.ceil(this.todosResultados.length / this.itensPorPagina);
    },
  },
  methods: {
    formatarCampo(valor) {
      return valor ? valor : "Nao disponível";
    },
    async buscarDados() {
      if (!this.termoBusca.trim()) {
        this.erro = "Digite um termo para buscar!";
        return;
      }

      this.carregando = true;
      this.erro = "";
      this.todosResultados = [];
      this.paginaAtual = 1;

      try {
        const resposta = await axios.get(
          `http://127.0.0.1:5000/search?q=${this.termoBusca}`
        );
        this.todosResultados = resposta.data;

        if (!this.todosResultados.length) {
          this.erro = `Nenhum resultado encontrado para "${this.termoBusca}"`;
        }
      } catch (error) {
        this.erro = "Erro ao buscar os dados. Tente novamente.";
      } finally {
        this.carregando = false;
      }
    },
    proximaPagina() {
      if (this.paginaAtual < this.totalPaginas) {
        this.paginaAtual++;
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    },
    paginaAnterior() {
      if (this.paginaAtual > 1) {
        this.paginaAtual--;
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    },
  },
};
</script>


<style scoped>
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.status {
  padding: 15px;
  margin: 15px 0;
  border-radius: 4px;
  text-align: center;
}

.status.loading {
  background-color: #e3f2fd;
  color: #1976d2;
}

.status.error {
  background-color: #ffebee;
  color: #d32f2f;
}

.results-container {
  margin-top: 30px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination-controls button {
  padding: 5px 15px;
}

.results-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

.operadora-card {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
  transition: box-shadow 0.3s;
}

.operadora-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.operadora-info h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.operadora-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  color: #666;
  font-size: 14px;
}

.operadora-details div {
  margin-bottom: 5px;
}

@media (max-width: 768px) {
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .operadora-details {
    grid-template-columns: 1fr;
  }
}
</style>
