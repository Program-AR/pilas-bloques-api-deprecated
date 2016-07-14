VERSION=0.0.1
NAME=pilas-bloques-api

N=[0m
G=[01;32m
Y=[01;33m
B=[01;34m
R=[01;31m

all:
	@echo ""
	@echo "${B}Comandos para ${G}${NAME} ${B}v${VERSION}"
	@echo ""
	@echo "  ${R}IMPORTANTE: Leer README.md antes de ejecutar cualquier comando.${N}"
	@echo ""
	@echo "  ${Y}Para desarrolladores ${N}"
	@echo ""
	@echo "    ${G}init${N}         Instala todas las dependencias."
	@echo "    ${G}initdb${N}       Genera la base de datos desde cero."
	@echo "    ${G}test${N}         Corre los tests una sola vez."
	@echo "    ${G}list${N}         Emite un listado de todas las soluciones almacenadas."
	@echo "    ${G}watch${N}        Corre los tests de forma contínua."
	@echo ""
	@echo "  ${Y}Para administradores ${N}"
	@echo ""
	@echo "    ${G}run${N}          Ejecuta la aplicación."
	@echo ""

init:
	pip install -r requirements.txt

initdb:
	python initdb.py

test:
	nosetests tests.py --rednose --force-color --nocapture

watch:
	nosetests --with-watch tests.py --rednose --force-color

list:
	@python list.py

run:
	@python run.py
