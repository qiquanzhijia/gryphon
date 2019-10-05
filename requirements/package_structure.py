gryphon 
    > execution 
        > bots
            > overwatch
                > def watch()
                > def check_profit(db)
                > def check_open_pl(db)
                > def check_ticktimes(db)
                > def check_position(db)
                > def check_btc_net_assets(db)
                > def check_spreads_are_normal(db)
                > def check_fv_not_stagnant(db)
                > def check_fv_predictor_key_set(r)
                > def succeeed(check_id)
                > def fail(check_id, detail_msg)
            > bank 
                > def run()
                > def audit_bmo_accounts(db)
                > def audit_boa_accounts(db)
                > def audit_bank_accounts(db, scraper)
                > def find_new_transactions(transactions, balance_diff)
                > def do_transactions_match(db_transaction, bank_transaction)
                > def record_transactions(db_account, transactions, db)
                > def notify_on_call_dev(transaction, db_account)
                > def record_burn(db_account, transaction, db)
                > def record_reverse_burn(db_account, transaction, db)
                > def account_num_to_key(account_num)
                > def key_to_account_num(key)
                > def load_accounts_map()
                > def success(name)
            > shoebox
                > def run()
                > def get_breaking_bitcoin_news()
                > def update_tx_hashes(db)
                > def in_progress_transactions(db)
                > def load_devs()
                > def dev_checkins()
                > def dev_summaries()
                > def is_end_of_workday(current_time, dev)
                > def is_workday(current_time)
                > def is_working(current_time, dev)
                > def message_dev_for_summary(dev)
                > def message_dev_for_checkin(dev, current_time)
                > def clock_emoji(time)
                > def fun_emoji()
                > def fun_bot_name(emoji) 
                > def manual_btc_withdrawals(db)
                > def btc_withdrawal_notification(exchange_db, amount)
                > def money_moving()
                > def notify_revenue(db)
                > def get_on_call_dev()

