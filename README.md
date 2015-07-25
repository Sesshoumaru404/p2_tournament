###Project 2: Swiss Tournament
This project was used to help me with writing a Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.
Project 2 was designed to teach you how to create and use databases through the use of database schemas and how to manipulate the data inside the database. This project has two parts: defining the database schema (SQL table definitions) in tournament.sql, and writing code that will use it to track a Swiss tournament in tournament.py.


###Files
| File | Description |
|------|-------------|
| **Vagrantfile** | This is file is used to create virtual box to run project in. |
| **pg_config.sh** | This is file is used to configure your virtual box. |
| **/tournament/tournament.py** | This is the main Python file used to conduct the Swiss Style Tournament. |
| **/tournament/tournament.sql** | Where you will find the database schema, in the form of SQL create table commands |
| **/tournament/tournament_test.py** | Contains test functions that will test the functions you’ve written in tournament.py |
| **/tournament/tournament_extra.py** | A Python file that will simulate tournaments that has all the requires listed for extra credit. |

###Requirements
* Virtual Box - [download](https://www.virtualbox.org/wiki/Downloads)
* Vagrant - [download](https://www.vagrantup.com/downloads)

####Installation Steps:
1. Download project:
  - Linux: Open terminal the type `git clone https://github.com/Sesshoumaru404/p2_tournament.git`
2. Move to project folder:
  - Linux: Type `cd p2_tournament/tournament`
3. Turn on the virtual machine:
  - Linux: Type `vagrant up`
  - Linux: Followed by `vagrant ssh`
  - You are now in your Virtual Machine.
4. Move to the *tournament* folder:
  - Vagrant terminal: Type `cd /vagrant/tournament`

###Tests
1. To run tests or extra credit:
  - Vagrant terminal: Type `python tournament_test.py`
    - This will output the test results.
  - Vagrant terminal: Type `python tournament_extra.py`
    - This will output 3 tournament results.
    ```
    Tournament Fake_Tournament_0 with 9 players will lasted 4 rounds.
    Final Results
    1. Shazman with 10 pionts and record of 3 - 1 - 0 omw 5
    2. Superman with 7 pionts and record of 2 - 1 - 1 omw 6
    3. Green_Lantern with 6 pionts and record of 1 - 3 - 0 omw 4
    4. Atom with 6 pionts and record of 1 - 3 - 0 omw 4
    5. Flash with 5 pionts and record of 1 - 2 - 1 omw 6
    6. Aquaman with 5 pionts and record of 1 - 2 - 1 omw 6
    7. Cycborg with 5 pionts and record of 1 - 2 - 1 omw 5
    8. Batman with 4 pionts and record of 1 - 1 - 2 omw 5
    9. Wonder_Woman with 4 pionts and record of 1 - 1 - 2 omw 3
    ```

###Functions
Need functions help check out [wiki](https://github.com/Sesshoumaru404/p2_tournament/wiki/Functions).

###License

MIT
