# 🤖 MCP PROPOSTA KILLER - GUIA DE USO

## O Kit Proposta Killer agora é um MCP Server interativo!

---

## 🎯 O QUE É ESTE MCP?

Um servidor MCP que transforma o Kit Proposta Killer em ferramentas interativas que você pode usar diretamente no Cursor ou qualquer cliente MCP.

**Ao invés de:** Preencher templates manualmente  
**Você faz:** Chama funções que fazem o trabalho pesado por você

---

## ⚙️ INSTALAÇÃO

### **1. Copie os arquivos necessários**
```bash
# Certifique-se que estes arquivos estão na raiz do projeto:
- mcp_proposta_killer.py
- mcp_proposta_killer_config.json
```

### **2. Configure no Cursor**

Adicione ao seu arquivo de configuração MCP do Cursor:

**Windows:** `%APPDATA%\Cursor\User\globalStorage\mcp\config.json`  
**Mac/Linux:** `~/.config/Cursor/User/globalStorage/mcp/config.json`

```json
{
  "mcpServers": {
    "proposta-killer": {
      "command": "python",
      "args": ["C:/caminho/completo/para/mcp_proposta_killer.py"],
      "description": "Ferramentas para criação de propostas comerciais"
    }
  }
}
```

### **3. Reinicie o Cursor**

Após adicionar a configuração, reinicie o Cursor para carregar o servidor MCP.

---

## 🛠️ FERRAMENTAS DISPONÍVEIS

### **1. 📋 analisar_cliente**

Analisa informações do cliente e retorna insights estruturados

**Como usar no Cursor:**
```
@analisar_cliente {
  "empresa": "Assisconsult",
  "segmento": "Consultoria de TI",
  "colaboradores": 110,
  "dores": [
    "Fechamento de folha leva 5 dias",
    "Documentos enviados por WhatsApp",
    "Gestão manual de atestados"
  ],
  "ferramentas_atuais": [
    {"nome": "Sistema de ponto básico", "custo_mensal": 700}
  ],
  "orcamento": 2000,
  "objetivos": ["Crescer 20-30%", "Modernizar RH"]
}
```

**Retorna:**
- Classificação de porte da empresa
- Plano recomendado (Starter/Planning/Enterprise)
- Dores priorizadas por impacto
- Score de urgência (0-100)
- Recomendações personalizadas

---

### **2. 💰 calcular_roi**

Calcula ROI com 3 métodos diferentes

**Como usar no Cursor:**
```
@calcular_roi {
  "processos_manuais": [
    {
      "nome": "Fechamento de folha",
      "tempo_atual_h": 40,
      "tempo_com_solucao_h": 8
    },
    {
      "nome": "Distribuição de documentos",
      "tempo_atual_h": 16,
      "tempo_com_solucao_h": 2
    },
    {
      "nome": "Gestão de atestados",
      "tempo_atual_h": 12,
      "tempo_com_solucao_h": 2
    }
  ],
  "custo_hora_equipe": 50,
  "ferramentas_substituidas": [
    {"nome": "Sistema ponto", "custo_mensal": 700}
  ],
  "custo_solucao_mensal": 1571.63,
  "custo_implementacao": 1200,
  "riscos_evitados": [
    {
      "nome": "Processo trabalhista",
      "probabilidade_pct": 30,
      "custo_se_ocorrer": 50000
    },
    {
      "nome": "Multa LGPD",
      "probabilidade_pct": 10,
      "custo_se_ocorrer": 100000
    }
  ]
}
```

**Retorna:**
- Economia de tempo detalhada por processo
- Redução de custos vs ferramentas atuais
- Valor de riscos evitados
- ROI percentual e payback em meses
- Mensagens prontas para usar na proposta

---

### **3. ✅ validar_proposta**

Valida qualidade da proposta com checklist

**Como usar no Cursor:**
```
@validar_proposta {
  "tem_nome_cliente": true,
  "tem_dores_especificas": true,
  "tem_roi_calculado": true,
  "tem_preco_claro": true,
  "tem_tabela_antes_depois": true,
  "tem_objecoes_respondidas": false,
  "tem_call_to_action": true,
  "tem_cronograma": true,
  "testado_mobile": false,
  "revisao_ortografica": true
}
```

**Retorna:**
- Score de qualidade (0-100)
- Classificação (Excelente/Boa/Regular/Precisa Melhorar)
- Lista do que está faltando
- Recomendações específicas de melhoria

---

### **4. 💡 sugerir_secoes**

Sugere seções relevantes baseadas no contexto

**Como usar no Cursor:**
```
@sugerir_secoes {
  "segmento": "Tecnologia",
  "dores_principais": [
    "Processos manuais demorados",
    "Falta de integração entre sistemas",
    "Risco de compliance"
  ],
  "objecoes_esperadas": [
    "Preço maior que atual",
    "Concorrente oferece cashback"
  ],
  "porte": "média empresa"
}
```

**Retorna:**
- Seções sugeridas com prioridade
- Motivo de cada sugestão
- Template recomendado para cada seção
- Ordem ideal das seções na proposta

---

### **5. 📧 gerar_email_envio**

Gera email personalizado para envio

**Como usar no Cursor:**
```
@gerar_email_envio {
  "nome_cliente": "Anderson",
  "empresa": "Assisconsult",
  "dor_principal": "eliminar processos manuais de RH",
  "beneficio_1": "Economiza 68,5 horas/mês da equipe de RH",
  "beneficio_2": "Reduz fechamento de folha de 5 dias para horas",
  "beneficio_3": "Garante compliance com LGPD e CLT",
  "investimento_mensal": "1.571,63",
  "roi_percentual": 153,
  "payback_meses": 7.8,
  "data_call": "quinta-feira",
  "hora_call": "14h",
  "seu_nome": "Victor Gutierrez",
  "seu_contato": "+55 11 98765-4321"
}
```

**Retorna:**
- Email completo formatado
- Assunto otimizado
- Destaques principais
- Call-to-action claro

---

## 🎓 EXEMPLOS DE USO PRÁTICO

### **WORKFLOW COMPLETO NO CURSOR:**

#### **1. Após reunião com cliente:**
```
Analise este cliente para mim:

@analisar_cliente {
  "empresa": "TechStartup",
  "segmento": "SaaS",
  "colaboradores": 45,
  "dores": [
    "Planilhas de vendas desorganizadas",
    "Falta de visibilidade do funil",
    "Follow-ups perdidos"
  ],
  "orcamento": 5000,
  "objetivos": ["Aumentar conversão em 30%"]
}
```

#### **2. Calcular ROI:**
```
Com base na análise, calcule o ROI:

@calcular_roi {
  "processos_manuais": [
    {"nome": "Busca de dados", "tempo_atual_h": 80, "tempo_com_solucao_h": 10},
    {"nome": "Follow-ups manuais", "tempo_atual_h": 40, "tempo_com_solucao_h": 5}
  ],
  "custo_hora_equipe": 75,
  "custo_solucao_mensal": 4500,
  "custo_implementacao": 2000
}
```

#### **3. Sugerir estrutura:**
```
Sugira seções para esta proposta:

@sugerir_secoes {
  "segmento": "SaaS",
  "dores_principais": ["Desorganização", "Falta de visibilidade"],
  "objecoes_esperadas": ["Custo de implementação"],
  "porte": "startup"
}
```

#### **4. Validar antes de enviar:**
```
Valide minha proposta:

@validar_proposta {
  "tem_nome_cliente": true,
  "tem_dores_especificas": true,
  "tem_roi_calculado": true,
  "tem_preco_claro": true,
  "tem_tabela_antes_depois": true,
  "tem_objecoes_respondidas": true,
  "tem_call_to_action": true,
  "tem_cronograma": true,
  "testado_mobile": true,
  "revisao_ortografica": true
}
```

#### **5. Gerar email de envio:**
```
Gere o email de envio:

@gerar_email_envio {
  "nome_cliente": "Carlos",
  "empresa": "TechStartup",
  "dor_principal": "organizar o funil de vendas",
  "beneficio_1": "Economiza 110h/mês da equipe comercial",
  "beneficio_2": "Aumenta conversão em 30%",
  "beneficio_3": "Zero leads esquecidos",
  "investimento_mensal": "4.500",
  "roi_percentual": 245,
  "payback_meses": 4.2
}
```

---

## 🔥 CASOS DE USO

### **CASO 1: Cliente novo, pouco tempo**
```
1. @analisar_cliente (entender contexto)
2. @sugerir_secoes (estruturar proposta)
3. Criar proposta com sugestões
4. @gerar_email_envio (enviar)
```

### **CASO 2: Proposta complexa, precisa impressionar**
```
1. @analisar_cliente (análise profunda)
2. @calcular_roi (todos os 3 métodos)
3. @sugerir_secoes (estrutura personalizada)
4. Criar proposta completa
5. @validar_proposta (garantir qualidade)
6. @gerar_email_envio (envio profissional)
```

### **CASO 3: Revisar proposta existente**
```
1. @validar_proposta (checklist de qualidade)
2. Corrigir pontos faltantes
3. @validar_proposta novamente (confirmar score alto)
```

---

## 💡 DICAS AVANÇADAS

### **Combinar ferramentas:**
```
Faça análise completa:

1. @analisar_cliente {...}
2. Use o resultado para @calcular_roi {...}
3. Use ambos para @sugerir_secoes {...}
4. Crie a proposta
5. @validar_proposta {...}
6. Se score < 80, corrija e valide novamente
7. @gerar_email_envio {...}
```

### **Iterar rapidamente:**
```
# Primeira versão rápida
@sugerir_secoes { porte: "pequena" }

# Versão melhorada
@sugerir_secoes { 
  porte: "pequena",
  dores_principais: [...],
  objecoes_esperadas: [...]
}
```

### **Validar durante criação:**
```
# A cada seção criada, valide
@validar_proposta {
  tem_nome_cliente: true,
  tem_dores_especificas: true,
  tem_roi_calculado: false,  // ainda não fiz
  ...
}
```

---

## 🐛 TROUBLESHOOTING

### **"Servidor MCP não está respondendo"**
```bash
# Verifique se o Python está no PATH
python --version

# Teste o servidor manualmente
python mcp_proposta_killer.py
```

### **"Tool not found"**
```
# Verifique se o nome está correto:
- analisar_cliente ✅
- calcular_roi ✅
- validar_proposta ✅
- sugerir_secoes ✅
- gerar_email_envio ✅
```

### **"Invalid JSON"**
```
# Use sempre aspas duplas em JSON
{"nome": "Teste"}  ✅
{'nome': 'Teste'}  ❌
```

---

## 📈 PRÓXIMAS FEATURES (Roadmap)

- [ ] `gerar_proposta_html` - Gera HTML completo automaticamente
- [ ] `comparar_propostas` - Compara versões A/B
- [ ] `exportar_pdf` - Gera PDF direto do MCP
- [ ] `buscar_cases` - Sugere cases similares
- [ ] `calcular_desconto_ideal` - Otimiza pricing
- [ ] `prever_taxa_conversao` - ML para prever sucesso

---

## 🤝 CONTRIBUINDO

Quer adicionar mais ferramentas ao MCP?

1. Edite `mcp_proposta_killer.py`
2. Adicione nova função na classe `PropostaKillerMCP`
3. Registre no método `handle_request`
4. Teste e documente aqui

---

## 📞 SUPORTE

**Dúvidas sobre o MCP?**
- Consulte a documentação MCP oficial
- Verifique logs do Cursor
- Teste as funções isoladamente

**Dúvidas sobre as ferramentas?**
- Revise os exemplos acima
- Veja o código fonte em `mcp_proposta_killer.py`
- Consulte os arquivos do Kit Proposta Killer

---

## ⭐ FEEDBACK

Está usando o MCP? Conte sua experiência:

**O que está funcionando bem?**
**O que pode melhorar?**
**Que ferramenta gostaria de ver adicionada?**

---

**Versão:** 1.0.0  
**Última atualização:** 30/09/2025  
**Compatível com:** MCP Protocol 1.0+

---

**🚀 Agora suas propostas têm superpoderes!**

*De templates manuais para IA assistida em segundos.*
