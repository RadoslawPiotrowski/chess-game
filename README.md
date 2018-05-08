# chess-game
Its is the simply chess game which i am already creating. I am in the middle of my way to finish this project and it's not ended version but it shows my programming skills and knowledge in python language.

## Git w kilku komendach

### Pierwsze kroki

git clone https://github.com/RadoslawPiotrowski/chess-game.git - pobranie repozytorium

git config --global user.name "John Doe" - ustawienie nazwy autora commitów

git config --global user.email "john@example.com" - ustawienie maila autora commitów


### Komunikacja z serwerem

git pull - ściągnięcie z serwera zmian na bieżącej gałęzi

git fetch - ściągnięcie z serwera zmian na wszystkich gałęziach

git push - wypchnięcie zcommitowanych zmian na serwer


### Operacje na gałęziach

git checkout <nazwa gałęzi> - zmiana gałęzi na inną istniejącą

git checkout -b <nazwa gałęzi> - stworzenie nowej gałęzi

git branch - lista gałęzi

git branch -d - usunięcie gałęzi lokalnie (na serwerze można usunąć przez GUI)


### Obsługa commita

git status - stan lokalnego repo - lista zmienionych plików, różnice między origin a local

git add <filename> - dodanie pliku do potencjalnego commita

git remove <filename> - usunięcie pliku z potencjalnego commita

git add . - dodanie wszystkiego jak leci do potencjalnego commita (niebezpieczne, czasem można dodać niechciany plik)

git commit -m "Opis commita" - stworzenie commita 

git commit --amend -m "New commit message" - zmiana opisu ostatniego commita

git merge <gałąź źródłowa> - wrzucenie zmian z innej gałęzi na naszą

git diff <nazwa pliku lub commita> - wyświetlenie zmian danego pliku od ostaniego commita

git diff - wyświetlenie różnic we wszystkich plikach od ostatniego commita

git reset --hard - cofnięcie się do stanu z poprzedniego commita

git log - lista ostatnich commitów na danej gałęzi
