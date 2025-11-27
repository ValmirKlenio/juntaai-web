import React, { useState, useEffect } from 'react'
import { obterPerguntas, enviarQuestionario } from '../utils/api'

function Questionario({ modoTEA, setSecaoAtiva }) {
  const [perguntas, setPerguntas] = useState([])
  const [respostas, setRespostas] = useState({})
  const [perguntaAtual, setPerguntaAtual] = useState(0)
  const [carregando, setCarregando] = useState(true)
  const [enviando, setEnviando] = useState(false)
  const [resultado, setResultado] = useState(null)
  const [erro, setErro] = useState(null)

  useEffect(() => {
    carregarPerguntas()
  }, [])

  const carregarPerguntas = async () => {
    try {
      const data = await obterPerguntas()
      setPerguntas(data)
      setCarregando(false)
    } catch (error) {
      setErro('Erro ao carregar perguntas. Tente novamente.')
      setCarregando(false)
    }
  }

  const handleResposta = (perguntaId, resposta) => {
    setRespostas({
      ...respostas,
      [perguntaId]: resposta,
    })
  }

  const proximaPergunta = () => {
    if (perguntaAtual < perguntas.length - 1) {
      setPerguntaAtual(perguntaAtual + 1)
    }
  }

  const perguntaAnterior = () => {
    if (perguntaAtual > 0) {
      setPerguntaAtual(perguntaAtual - 1)
    }
  }

  const handleEnviar = async () => {
    if (Object.keys(respostas).length !== perguntas.length) {
      alert('Por favor, responda todas as perguntas antes de enviar.')
      return
    }

    setEnviando(true)
    try {
      const result = await enviarQuestionario(respostas)
      setResultado(result)
    } catch (error) {
      setErro('Erro ao enviar questionário. Tente novamente.')
    } finally {
      setEnviando(false)
    }
  }

  if (carregando) {
    return (
      <section className="questionario-section">
        <div className="container">
          <div className="loading">Carregando questionário...</div>
        </div>
      </section>
    )
  }

  if (erro) {
    return (
      <section className="questionario-section">
        <div className="container">
          <div className="erro">{erro}</div>
        </div>
      </section>
    )
  }

  if (resultado) {
    return (
      <section className="questionario-section">
        <div className="container">
          <div className={`resultado resultado-${resultado.nivel_risco}`}>
            <h2>Resultado do Questionário</h2>
            <div className="resultado-icon">
              {resultado.nivel_risco === 'alto' && '🚨'}
              {resultado.nivel_risco === 'medio' && '⚠️'}
              {resultado.nivel_risco === 'baixo' && '✅'}
            </div>
            <p className="resultado-mensagem">{resultado.mensagem}</p>

            {resultado.nivel_risco === 'alto' && (
              <div className="alerta-urgente">
                <h3>⚠️ Sinais de Risco Elevado</h3>
                <p>
                  Suas respostas indicam que você pode estar em uma situação de violência. Por
                  favor, considere entrar em contato com os recursos de apoio disponíveis.
                </p>
                <button
                  className="btn btn-primary btn-large"
                  onClick={() => setSecaoAtiva('apoio')}
                >
                  Ver Recursos de Apoio
                </button>
              </div>
            )}

            {resultado.nivel_risco === 'medio' && (
              <div className="alerta-atencao">
                <h3>Fique Atenta aos Sinais</h3>
                <p>
                  Algumas situações que você relatou merecem atenção. Converse com alguém de
                  confiança ou busque orientação profissional.
                </p>
              </div>
            )}

            <div className="acoes-resultado">
              <button className="btn btn-secondary" onClick={() => setSecaoAtiva('apoio')}>
                Ver Rede de Apoio
              </button>
              <button className="btn btn-outline" onClick={() => setSecaoAtiva('home')}>
                Voltar ao Início
              </button>
            </div>

            <div className="info-box">
              <p>
                <strong>Lembre-se:</strong> Este questionário é uma ferramenta de auto-avaliação e
                não substitui orientação profissional. Se você se sente em perigo, ligue 190 ou 180.
              </p>
            </div>
          </div>
        </div>
      </section>
    )
  }

  const pergunta = perguntas[perguntaAtual]
  const progresso = ((perguntaAtual + 1) / perguntas.length) * 100

  return (
    <section className="questionario-section">
      <div className="container">
        <div className="questionario-header">
          <h2>Questionário de Auto-Avaliação</h2>
          <p>Responda com sinceridade. Suas respostas são completamente anônimas.</p>
          <div className="progresso-bar">
            <div className="progresso-fill" style={{ width: `${progresso}%` }}></div>
          </div>
          <p className="progresso-texto">
            Pergunta {perguntaAtual + 1} de {perguntas.length}
          </p>
        </div>

        <div className="pergunta-card">
          <h3 className="pergunta-texto">{pergunta.texto}</h3>

          <div className="opcoes-lista">
            {pergunta.opcoes.map((opcao, index) => (
              <button
                key={index}
                className={`opcao-btn ${respostas[pergunta.id] === opcao ? 'selected' : ''}`}
                onClick={() => handleResposta(pergunta.id, opcao)}
              >
                <span className="opcao-radio"></span>
                <span className="opcao-texto">{opcao}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="questionario-navegacao">
          <button
            className="btn btn-outline"
            onClick={perguntaAnterior}
            disabled={perguntaAtual === 0}
          >
            ← Anterior
          </button>

          {perguntaAtual < perguntas.length - 1 ? (
            <button
              className="btn btn-primary"
              onClick={proximaPergunta}
              disabled={!respostas[pergunta.id]}
            >
              Próxima →
            </button>
          ) : (
            <button
              className="btn btn-primary"
              onClick={handleEnviar}
              disabled={Object.keys(respostas).length !== perguntas.length || enviando}
            >
              {enviando ? 'Enviando...' : 'Finalizar Questionário'}
            </button>
          )}
        </div>

        <div className="info-box mt-4">
          <p>
            <strong>🔒 Privacidade:</strong> Suas respostas são armazenadas de forma anônima e
            utilizadas apenas para gerar estatísticas agregadas que ajudam em pesquisas sobre
            violência.
          </p>
        </div>
      </div>
    </section>
  )
}

export default Questionario
