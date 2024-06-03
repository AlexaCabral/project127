Go account using cd account (and also in the MariaDB terminal)

Login to MariaDB using:

Run `mysql -u root -p<your_password>`

Then, run

```SOURCE project.sql```

After, use the project database using:

```USE project```

Now the database is set-up.

To manage food items, food establishments, food reviews, customer, owner accounts: run 

```python customer_login_account.py```

To view reports for whole database: run

```python reports.py```
