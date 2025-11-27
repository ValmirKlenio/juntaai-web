import React, { useState, useEffect } from 'react'
import { obterRecursosApoio } from '../utils/api'

function RedeApoio({ modoTEA }) {
  const [recursos, setRecursos] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState(null)

  useEffect(() => {
    carregarRecursos()
  }, [])

  const carregarRecursos = async () => {
    try {
      const data = await obterRecursosApoio()
      setRecursos(data)
      setCarregando(false)
    } catch (error) {
      setErro('Erro ao carregar recursos.')
      setCarregando(false)
    }
  }

  if (carregando) {
    return (
      <section className="apoio-section">
        <div className="container">
          <div className="loading">Carregando recursos...</div>
        </div>
      </section>
    )
  }

  if (erro) {
    return (
      <section className="apoio-section">
        <div className="container">
          <div className="erro">{erro}</div>
        </div>
      </section>
    )
  }

  const recursosEmergencia = recursos.filter((r) => r.tipo === 'emergencia')
  const recursosPoliciais = recursos.filter((r) => r.tipo === 'policial')
  const recursosApoio = recursos.filter((r) => r.tipo === 'apoio')

  return (
    <section className="apoio-section">
      <div className="container">
        <h2>Rede de Apoio e Recursos</h2>
        <p className="subtitulo">
          Você não está sozinha. Existem diversos recursos disponíveis para te ajudar de forma
          segura e confidencial.
        </p>

        <div className="alerta-emergencia">
          <div className="alerta-icon">🚨</div>
          <div className="alerta-conteudo">
            <h3>Em caso de emergência imediata:</h3>
            <p>Se você está em perigo agora, ligue:</p>
            <div className="telefones-emergencia">
              <a href="tel:190" className="telefone-btn">
                190 - Polícia Militar
              </a>
              <a href="tel:180" className="telefone-btn">
                180 - Central da Mulher
              </a>
            </div>
          </div>
        </div>

        <div className="recursos-container">
          <h3>📞 Linhas de Atendimento</h3>
          <div className="recursos-grid">
            {recursosEmergencia.map((recurso) => (
              <div key={recurso.id} className="recurso-card emergencia">
                <h4>{recurso.nome}</h4>
                <p>{recurso.descricao}</p>
                {recurso.telefone && (
                  <a href={`tel:${recurso.telefone}`} className="telefone-link">
                    📞 {recurso.telefone}
                  </a>
                )}
              </div>
            ))}
          </div>

          <h3>🏛️ Delegacias e Serviços Policiais</h3>
          <div className="recursos-grid">
            {recursosPoliciais.map((recurso) => (
              <div key={recurso.id} className="recurso-card policial">
                <h4>{recurso.nome}</h4>
                <p>{recurso.descricao}</p>
                {recurso.telefone && (
                  <a href={`tel:${recurso.telefone}`} className="telefone-link">
                    📞 {recurso.telefone}
                  </a>
                )}
              </div>
            ))}
          </div>

          <h3>🤝 Centros de Apoio e Acolhimento</h3>
          <div className="recursos-grid">
            {recursosApoio.map((recurso) => (
              <div key={recurso.id} className="recurso-card apoio">
                <h4>{recurso.nome}</h4>
                <p>{recurso.descricao}</p>
                {recurso.telefone && (
                  <a href={`tel:${recurso.telefone}`} className="telefone-link">
                    📞 {recurso.telefone}
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="info-box">
          <h3>💡 Dicas de Segurança</h3>
          <ul>
            <li>Mantenha documentos importantes em lugar seguro (RG, CPF, certidões)</li>
            <li>Tenha um plano de saída caso precise sair rapidamente de casa</li>
            <li>Confie em amigos ou familiares de confiança sobre sua situação</li>
            <li>Registre evidências (fotos de lesões, mensagens ameaçadoras)</li>
            <li>Saiba que você pode solicitar medidas protetivas na delegacia</li>
            <li>Não se culpe - a violência nunca é culpa da vítima</li>
          </ul>
        </div>

        <div className="info-box">
          <h3>⚖️ Seus Direitos</h3>
          <p>
            A <strong>Lei Maria da Penha (Lei 11.340/2006)</strong> protege mulheres em situação de
            violência doméstica. Você tem direito a:
          </p>
          <ul>
            <li>Medidas protetivas de urgência</li>
            <li>Atendimento pela Polícia e Delegacia da Mulher</li>
            <li>Acompanhamento psicológico e social</li>
            <li>Acesso à Defensoria Pública gratuita</li>
            <li>Abrigo em casas de proteção</li>
          </ul>
        </div>
      </div>
    </section>
  )
}

export default RedeApoio
