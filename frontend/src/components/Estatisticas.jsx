import React, { useState, useEffect } from 'react'
import { obterEstatisticas } from '../utils/api'

function Estatisticas({ modoTEA }) {
  const [stats, setStats] = useState(null)
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState(null)

  useEffect(() => {
    carregarEstatisticas()
  }, [])

  const carregarEstatisticas = async () => {
    try {
      const data = await obterEstatisticas()
      setStats(data)
      setCarregando(false)
    } catch (error) {
      setErro('Erro ao carregar estatísticas.')
      setCarregando(false)
    }
  }

  if (carregando) {
    return (
      <section className="estatisticas-section">
        <div className="container">
          <div className="loading">Carregando estatísticas...</div>
        </div>
      </section>
    )
  }

  if (erro) {
    return (
      <section className="estatisticas-section">
        <div className="container">
          <div className="erro">{erro}</div>
        </div>
      </section>
    )
  }

  return (
    <section className="estatisticas-section">
      <div className="container">
        <h2>Estatísticas e Dados</h2>
        <p className="subtitulo">
          Dados agregados e anônimos que ajudam a entender e combater a violência em
          relacionamentos.
        </p>

        <div className="stats-grid">
          <div className="stat-card destacado">
            <div className="stat-icon">📊</div>
            <div className="stat-numero">{stats.total_respostas}</div>
            <div className="stat-label">Questionários Respondidos</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🔍</div>
            <div className="stat-label">Dados para Pesquisa</div>
            <p>
              Todas as respostas são armazenadas de forma anônima e contribuem para estudos sobre
              violência doméstica e de gênero.
            </p>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🎓</div>
            <div className="stat-label">Para Estudantes</div>
            <p>
              Pesquisadores e estudantes podem utilizar esses dados agregados em trabalhos
              acadêmicos sobre o tema.
            </p>
          </div>
        </div>

        <div className="info-box">
          <h3>📈 Dados Nacionais Sobre Violência</h3>
          <ul>
            <li>
              <strong>1 em cada 3 mulheres</strong> no mundo já sofreu violência física ou sexual
              por parceiro íntimo (OMS)
            </li>
            <li>
              No Brasil, uma mulher é agredida a cada <strong>2 minutos</strong> (Fórum Brasileiro
              de Segurança Pública)
            </li>
            <li>
              <strong>80% dos casos</strong> de violência doméstica não são denunciados
            </li>
            <li>
              A violência psicológica afeta <strong>48%</strong> das mulheres em relacionamentos
              abusivos
            </li>
          </ul>
        </div>

        {stats.total_respostas > 0 && (
          <div className="analise-section">
            <h3>Análise de Respostas</h3>
            <p className="info-texto">
              Os dados abaixo mostram a distribuição das respostas de forma agregada e anônima:
            </p>
            <div className="analise-info">
              <p>
                Total de respostas coletadas: <strong>{stats.total_respostas}</strong>
              </p>
              <p className="texto-pequeno">
                * Para proteger a privacidade, análises detalhadas só são exibidas quando há um
                número significativo de respostas.
              </p>
            </div>
          </div>
        )}

        <div className="referencias-section">
          <h3>📚 Referências e Recursos para Pesquisa</h3>
          <div className="referencias-lista">
            <div className="referencia-item">
              <h4>Lei Maria da Penha (Lei 11.340/2006)</h4>
              <p>
                Lei brasileira que cria mecanismos para coibir a violência doméstica e familiar
                contra a mulher.
              </p>
            </div>
            <div className="referencia-item">
              <h4>OMS - Organização Mundial da Saúde</h4>
              <p>Dados globais sobre violência contra mulheres e estudos epidemiológicos.</p>
            </div>
            <div className="referencia-item">
              <h4>Fórum Brasileiro de Segurança Pública</h4>
              <p>Anuário Brasileiro de Segurança Pública com estatísticas nacionais.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Estatisticas
