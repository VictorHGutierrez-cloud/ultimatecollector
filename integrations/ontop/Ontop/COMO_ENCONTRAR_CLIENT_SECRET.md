# Como Encontrar o CLIENT_SECRET na Factorial

## 📍 Onde Está o CLIENT_SECRET?

O CLIENT_SECRET geralmente está na **mesma página** onde você vê o CLIENT_ID, mas pode estar:

### Opção 1: Na Página de Edição da Aplicação
1. Na página "Edit application" (onde você viu o CLIENT_ID)
2. Procure por uma seção chamada:
   - **"Client Secret"**
   - **"Secret"**
   - **"Application Secret"**
   - Ou um botão **"Show Secret"** / **"Reveal Secret"**

### Opção 2: Pode Estar Oculto
- Pode haver um botão **"Show"** ou **"Reveal"** ao lado do campo
- Ou um ícone de **olho** 👁️ para mostrar/ocultar
- Clique nele para revelar o secret

### Opção 3: Pode Estar em Outra Seção
- Role a página para baixo
- Procure em seções como:
  - **"Credentials"**
  - **"Authentication"**
  - **"OAuth Settings"**
  - **"API Settings"**

### Opção 4: Pode Precisar Gerar
- Se não encontrar, pode haver um botão:
  - **"Generate Secret"**
  - **"Create Secret"**
  - **"Reset Secret"**

## 🔍 O que Procurar

O CLIENT_SECRET geralmente:
- É uma string longa (similar ao CLIENT_ID)
- Pode ter caracteres especiais
- Pode estar em um campo de texto ou área de código
- Pode estar marcado como "sensitive" ou "confidential"

## ⚠️ Importante

- O CLIENT_SECRET é **diferente** para cada CLIENT_ID
- O CLIENT_SECRET antigo (do CLIENT_ID antigo) **não funciona** com o novo CLIENT_ID
- Você precisa do CLIENT_SECRET que corresponde ao CLIENT_ID: `NyFzeb2fUEvPKehzOyUh-SGKNy27uUR-KqxW1rhA4l4`

## 📸 Dica

Se você conseguir tirar uma foto da página completa (ou mais abaixo), posso ajudar a identificar onde está o CLIENT_SECRET!
