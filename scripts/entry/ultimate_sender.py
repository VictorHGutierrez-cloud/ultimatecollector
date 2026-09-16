#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ULTIMATE SENDER - MENU INTERATIVO
Envio de dados (push) para a API Factorial com base no OAS
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Adicionar o diretório raiz do projeto ao path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from ultimate_collector.senders.ultimate_sender import UltimateSender


class UltimateSenderMenu:
    """Menu interativo do Ultimate Sender"""

    def __init__(self):
        self.sender = UltimateSender()
        self.running = True

    def display_main_menu(self):
        print("\n" + "=" * 80)
        print("🚀 ULTIMATE SENDER - ENVIO PARA API FACTORIAL")
        print("   Envia dados com base no OAS (sem validação)")
        print("=" * 80)
        print("1. 📋 Listar categorias")
        print("2. 🔗 Listar endpoints de uma categoria")
        print("3. 📤 Enviar para endpoint")
        print("4. 🎲 Enviar dados aleatórios")
        print("5. ❌ Sair")
        print("=" * 80)

    def get_user_choice(self) -> int:
        try:
            choice = input("\n🎯 Escolha uma opção (1-5): ").strip()
            return int(choice) if choice.isdigit() else 0
        except (ValueError, KeyboardInterrupt):
            return 0

    def run(self):
        while self.running:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                if choice == 1:
                    self.list_categories()
                elif choice == 2:
                    self.list_endpoints()
                elif choice == 3:
                    self.send_to_endpoint()
                elif choice == 4:
                    self.send_random_data()
                elif choice == 5:
                    self.exit_program()
                else:
                    print("❌ Opção inválida! Tente novamente.")
            except KeyboardInterrupt:
                print("\n\n👋 Saindo...")
                break
            except Exception as e:
                print(f"\n❌ Erro inesperado: {e}")
                input("\n⏸️  Pressione Enter para continuar...")

    def list_categories(self):
        categories = self.sender.list_categories()
        print("\n📋 CATEGORIAS DISPONÍVEIS")
        print("-" * 50)
        for i, category in enumerate(categories, 1):
            print(f"   {i:2d}. {category}")
        input("\n⏸️  Pressione Enter para continuar...")

    def list_endpoints(self):
        category = self._choose_category()
        if not category:
            return

        endpoints = self.sender.list_endpoints(category)
        print(f"\n🔗 ENDPOINTS DE {category.upper()}")
        print("-" * 50)
        for i, (name, info) in enumerate(endpoints.items(), 1):
            methods = ",".join(info.get("methods", []))
            path = info.get("path", "")
            print(f"   {i:2d}. {name}  [{methods}]  ({path})")
        input("\n⏸️  Pressione Enter para continuar...")

    def send_to_endpoint(self):
        category = self._choose_category()
        if not category:
            return

        endpoints = self.sender.list_endpoints(category)
        if not endpoints:
            print("❌ Sem endpoints disponíveis nessa categoria.")
            input("\n⏸️  Pressione Enter para continuar...")
            return

        endpoint_name = self._choose_endpoint(endpoints)
        if not endpoint_name:
            return

        endpoint_def = self.sender.resolve_endpoint(category, endpoint_name)
        if not endpoint_def:
            print("❌ Endpoint não encontrado.")
            input("\n⏸️  Pressione Enter para continuar...")
            return

        method = self._choose_method(endpoint_def.get("methods", []))
        if not method:
            return

        param_values = self._prompt_path_params(endpoint_def.get("path_params", []))
        params = self._prompt_json("Parâmetros de query (JSON, vazio para não usar): ")
        data = None
        if method in ("post", "put", "patch", "delete"):
            data = self._prompt_json("Body JSON (vazio para não enviar body): ")

        endpoint_path = self.sender.build_endpoint_path(endpoint_def, param_values)
        response = self.sender.send(method, endpoint_path, params=params, data=data)

        if response is None:
            print("❌ Falha no envio.")
        elif response.get("_not_found"):
            print("⚠️ Endpoint não encontrado.")
        else:
            print("✅ Envio realizado!")
            print(json.dumps(response, indent=2, ensure_ascii=False)[:2000])

        input("\n⏸️  Pressione Enter para continuar...")

    def send_random_data(self):
        category = self._choose_category()
        if not category:
            return

        endpoints = self.sender.list_endpoints(category)
        if not endpoints:
            print("❌ Sem endpoints disponíveis nessa categoria.")
            input("\n⏸️  Pressione Enter para continuar...")
            return

        endpoint_name = self._choose_endpoint(endpoints)
        if not endpoint_name:
            return

        endpoint_def = self.sender.resolve_endpoint(category, endpoint_name)
        if not endpoint_def:
            print("❌ Endpoint não encontrado.")
            input("\n⏸️  Pressione Enter para continuar...")
            return

        method = self._choose_method(endpoint_def.get("methods", []))
        if not method:
            return

        param_values = self._prompt_path_params(endpoint_def.get("path_params", []))
        params = self._prompt_json("Parâmetros de query (JSON, vazio para não usar): ")
        data = self.sender.build_random_payload(endpoint_def, method)
        print("\n📦 Payload aleatório gerado:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] if data else "null")

        endpoint_path = self.sender.build_endpoint_path(endpoint_def, param_values)
        response = self.sender.send(method, endpoint_path, params=params, data=data)

        if response is None:
            print("❌ Falha no envio.")
        elif response.get("_not_found"):
            print("⚠️ Endpoint não encontrado.")
        else:
            print("✅ Envio realizado!")
            print(json.dumps(response, indent=2, ensure_ascii=False)[:2000])

        input("\n⏸️  Pressione Enter para continuar...")

    def _choose_category(self) -> Optional[str]:
        categories = self.sender.list_categories()
        if not categories:
            print("❌ Nenhuma categoria encontrada no OAS.")
            input("\n⏸️  Pressione Enter para continuar...")
            return None

        print("\n📋 CATEGORIAS")
        for i, category in enumerate(categories, 1):
            print(f"   {i:2d}. {category}")
        try:
            choice = int(input("\nEscolha uma categoria (número): ")) - 1
            if 0 <= choice < len(categories):
                return categories[choice]
            print("❌ Categoria inválida!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
        return None

    def _choose_endpoint(self, endpoints: Dict[str, Dict[str, Any]]) -> Optional[str]:
        endpoint_names = list(endpoints.keys())
        print("\n🔗 ENDPOINTS")
        for i, name in enumerate(endpoint_names, 1):
            methods = ",".join(endpoints[name].get("methods", []))
            print(f"   {i:2d}. {name} [{methods}]")
        try:
            choice = int(input("\nEscolha um endpoint (número): ")) - 1
            if 0 <= choice < len(endpoint_names):
                return endpoint_names[choice]
            print("❌ Endpoint inválido!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
        return None

    def _choose_method(self, methods):
        if not methods:
            print("❌ Endpoint sem métodos de escrita.")
            input("\n⏸️  Pressione Enter para continuar...")
            return None
        if len(methods) == 1:
            return methods[0]
        print("\n🧭 MÉTODOS DISPONÍVEIS")
        for i, method in enumerate(methods, 1):
            print(f"   {i}. {method.upper()}")
        try:
            choice = int(input("\nEscolha um método (número): ")) - 1
            if 0 <= choice < len(methods):
                return methods[choice]
            print("❌ Método inválido!")
        except ValueError:
            print("❌ Entrada inválida!")
        input("\n⏸️  Pressione Enter para continuar...")
        return None

    def _prompt_path_params(self, params):
        values = {}
        for name in params:
            value = input(f"Informe o valor para '{name}': ").strip()
            if value:
                values[name] = value
        return values

    def _prompt_json(self, prompt: str) -> Optional[Dict]:
        raw = input(prompt).strip()
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            print("❌ JSON inválido. Envie novamente.")
            return self._prompt_json(prompt)

    def exit_program(self):
        print("\n👋 OBRIGADO POR USAR O ULTIMATE SENDER!")
        self.running = False


def main():
    print("🚀 INICIANDO ULTIMATE SENDER...")
    menu = UltimateSenderMenu()
    menu.run()


if __name__ == "__main__":
    main()
