#!/usr/bin/env python3
"""
Script de teste para autenticação e uso da API da Maritaca
"""
import os
import sys
import json

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas"""
    try:
        import openai
        print(f"✅ Biblioteca openai instalada (versão: {openai.__version__})")
        return True, openai
    except ImportError:
        print("❌ Biblioteca 'openai' não encontrada!")
        print("\nInstale com: pip install openai")
        return False, None

def test_maritaca_auth():
    """Testa a autenticação e uma chamada simples à API da Maritaca"""
    
    # Verifica dependências
    deps_ok, openai = check_dependencies()
    if not deps_ok:
        return False
    
    print()
    
    # Verifica se a chave está configurada (tenta múltiplas opções)
    api_key = (
        os.environ.get("MARITALK_API_SECRET_KEY") or
        os.environ.get("CURSORMINIMAC") or
        os.environ.get("MARITACA_API_KEY")
    )
    
    if not api_key:
        print("❌ ERRO: Variável de ambiente da API não encontrada!")
        print("\n" + "="*60)
        print("📋 INSTRUÇÕES PARA CONFIGURAR:")
        print("="*60)
        print("\n1. Obtenha sua chave API em: https://plataforma.maritaca.ai/chaves-de-api")
        print("\n2. Configure uma das variáveis de ambiente:")
        print("   - MARITALK_API_SECRET_KEY (padrão)")
        print("   - CURSORMINIMAC (alternativa)")
        print("   - MARITACA_API_KEY (alternativa)")
        print("\n3. Configure de uma das formas:")
        print("\n   Opção A - Terminal (temporário):")
        print("   export CURSORMINIMAC='sua-chave-aqui'")
        print("   # ou")
        print("   export MARITALK_API_SECRET_KEY='sua-chave-aqui'")
        print("\n   Opção B - Arquivo .env (permanente):")
        print("   echo 'CURSORMINIMAC=sua-chave-aqui' >> .env")
        print("   source .env  # ou use python-dotenv")
        print("\n   Opção C - No shell atual:")
        print("   export CURSORMINIMAC='sua-chave-aqui'")
        print("   python test_maritaca_auth.py")
        print("\n" + "="*60)
        return False
    
    # Identifica qual variável foi usada
    used_var = None
    if os.environ.get("CURSORMINIMAC"):
        used_var = "CURSORMINIMAC"
    elif os.environ.get("MARITALK_API_SECRET_KEY"):
        used_var = "MARITALK_API_SECRET_KEY"
    elif os.environ.get("MARITACA_API_KEY"):
        used_var = "MARITACA_API_KEY"
    
    # Mostra apenas parte da chave por segurança
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
    print(f"✅ Chave API encontrada na variável: {used_var}")
    print(f"   Chave: {masked_key}")
    
    # Configura a API - tenta ambas as versões (v0.x e v1.x+)
    print("\n🔄 Testando conexão com a API da Maritaca...")
    print("   URL: https://chat.maritaca.ai/api")
    print("   Modelo de teste: sabia-3")
    
    # Detecta versão do openai
    openai_version = openai.__version__
    major_version = int(openai_version.split('.')[0])
    
    print(f"   Versão openai detectada: {openai_version}")
    
    try:
        if major_version >= 1:
            # API nova (v1.x+) - usa client
            print("   Usando API v1.x+ (client-based)")
            client = openai.OpenAI(
                api_key=api_key,
                base_url="https://chat.maritaca.ai/api"
            )
            response = client.chat.completions.create(
                model="sabia-3",
                messages=[
                    {"role": "user", "content": "Olá! Responda apenas 'OK' se você está funcionando."}
                ],
                max_tokens=10,
                temperature=0.0
            )
        else:
            # API antiga (v0.x) - usa módulo direto
            print("   Usando API v0.x (module-based)")
            openai.api_base = "https://chat.maritaca.ai/api"
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="sabia-3",
                messages=[
                    {"role": "user", "content": "Olá! Responda apenas 'OK' se você está funcionando."}
                ],
                max_tokens=10,
                temperature=0.0
            )
        
        print("\n✅ Autenticação bem-sucedida!")
        print(f"\n📝 Resposta da API:")
        
        # Extrai informações da resposta (compatível com ambas versões)
        try:
            if major_version >= 1:
                # API v1.x+
                model_name = response.model
                content = response.choices[0].message.content
                usage = response.usage
            else:
                # API v0.x
                model_name = response.get('model', 'N/A')
                if hasattr(response, 'choices'):
                    content = response.choices[0].message.content
                elif isinstance(response, dict) and 'choices' in response:
                    content = response['choices'][0]['message']['content']
                else:
                    content = str(response)
                usage = response.get('usage', {})
            
            print(f"   Modelo: {model_name}")
            print(f"   Resposta: {content}")
            if usage:
                print(f"   Tokens: {usage}")
        except Exception as e:
            print(f"   ⚠️  Erro ao extrair conteúdo: {e}")
            print(f"   Tipo da resposta: {type(response)}")
            if hasattr(response, '__dict__'):
                print(f"   Atributos: {list(response.__dict__.keys())[:10]}")
        
        # Mostra estrutura completa se solicitado
        if '--verbose' in sys.argv or '-v' in sys.argv:
            print(f"\n📊 Estrutura completa da resposta:")
            if major_version >= 1:
                # Converte objeto para dict
                response_dict = {
                    'model': response.model,
                    'choices': [{
                        'message': {
                            'role': c.message.role,
                            'content': c.message.content
                        }
                    } for c in response.choices],
                    'usage': {
                        'prompt_tokens': response.usage.prompt_tokens if response.usage else None,
                        'completion_tokens': response.usage.completion_tokens if response.usage else None,
                        'total_tokens': response.usage.total_tokens if response.usage else None,
                    } if response.usage else {}
                }
                print(json.dumps(response_dict, indent=2, ensure_ascii=False))
            else:
                print(json.dumps(response, indent=2, ensure_ascii=False, default=str))
        
        return True
        
    except (openai.error.AuthenticationError, openai.AuthenticationError) as e:
        print(f"\n❌ ERRO de Autenticação: {e}")
        print("\n💡 Verifique se:")
        print("   - A chave API está correta")
        print("   - A chave não expirou")
        print("   - Você tem permissão para usar a API")
        return False
        
    except (openai.error.APIError, openai.APIError) as e:
        print(f"\n❌ ERRO da API: {e}")
        print("\n💡 Verifique se:")
        print("   - A API está acessível")
        print("   - O modelo 'sabia-3' está disponível")
        print("   - Você tem créditos/quota disponível")
        return False
        
    except KeyError as e:
        print(f"\n❌ ERRO: Chave não encontrada na resposta: {e}")
        print("\n💡 A estrutura da resposta pode ser diferente do esperado.")
        print("   Execute com --verbose para ver a resposta completa:")
        print("   python test_maritaca_auth.py --verbose")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {type(e).__name__}: {e}")
        import traceback
        print("\n📋 Traceback completo:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DE AUTENTICAÇÃO - API MARITACA")
    print("=" * 60)
    
    success = test_maritaca_auth()
    
    print()
    print("=" * 60)
    if success:
        print("✅ TESTE CONCLUÍDO COM SUCESSO")
        print("\n🎉 A API da Maritaca está funcionando corretamente!")
        print("   Você pode usar o modelo 'maritalk' no projeto.")
    else:
        print("❌ TESTE FALHOU")
        print("\n💡 Verifique as instruções acima e tente novamente.")
    print("=" * 60)

