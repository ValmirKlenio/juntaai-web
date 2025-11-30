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

  // segurança: se não vier nada do back
  if (!stats) {
    return null
  }

  // rótulos bonitinhos para as categorias do back-end
  const labelsCategorias = {
    psicologica: 'Violência psicológica',
    fisica: 'Violência física',
    controle: 'Controle / isolamento',
    sexual: 'Violência sexual',
    ameaca: 'Ameaças / medo constante',
  }

  const categorias = stats.analise_categorias || {}

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
                * Para proteger a privacidade, os dados não identificam nenhuma pessoa
                individualmente.
              </p>

              {/* GRÁFICO DE BARRAS POR CATEGORIA */}
              {Object.keys(categorias).length > 0 && (
                <div className="grafico-categorias">
                  <h4>Distribuição por tipo de violência (respostas preocupantes)</h4>
                  <div className="grafico-legenda">
                    <span className="bolinha-legenda" /> Cada barra representa o percentual de
                    respostas com sinais de atenção em cada categoria.
                  </div>

                  <div className="grafico-lista">
                    {Object.entries(categorias).map(([chave, dados]) => (
                      <div className="grafico-linha" key={chave}>
                        <div className="grafico-label">{labelsCategorias[chave] || chave}</div>
                        <div className="grafico-barra-wrapper">
                          <div
                            className="grafico-barra"
                            style={{ width: `${dados.percentual}%` }}
                          ></div>
                        </div>
                        <div className="grafico-valor">{dados.percentual}%</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
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
