# Data Dictionary — Schema `transaction`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `transaction`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `inbox_id_seq` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_200` | `transaction` |  | needs_review | 109 | 109 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_accounthierarchy` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_accountinstance` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_assetcategory` | `transaction` |  | needs_review | 13 | 13 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_balancesumitem` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_balancesumitemmember` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_balancesumitemtrancode` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bankaccountlist` | `transaction` |  | needs_review | 5537 | 5537 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bankcash` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bankcashid` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_batchupload` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_batchuploaditem` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bsz` | `transaction` |  | needs_review | 63 | 63 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bszdetail` | `transaction` |  | needs_review | 435 | 435 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bsznumber` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bsztransaction` | `transaction` |  | needs_review | 83 | 83 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budget` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetitem` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetitemhierarchy` | `transaction` |  | needs_review | 2192 | 2192 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetowner` | `transaction` |  | needs_review | 17 | 17 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetownerhierarchy` | `transaction` |  | needs_review | 94 | 94 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetperiod` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetrevision` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgettransaction` | `transaction` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_cashflowgroup` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_cashflowmember` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_custom_idgen` | `transaction` |  | needs_review | 45 | 45 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dailybalance` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dailybalancecash` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dailyprojectbalance` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_deprassetid` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dinarcertificate` | `transaction` |  | needs_review | 4 | 4 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_distributiontransferinfo` | `transaction` |  | needs_review | 10 | 10 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donor` | `transaction` |  | needs_review | 4757 | 4757 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donorcommitment` | `transaction` |  | needs_review | 6 | 6 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donortotalfund` | `transaction` |  | needs_review | 4012 | 4012 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_employee` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_externaldebtor` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_externaltransaction` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_fact_daily_balance` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_fieldofwork` | `transaction` |  | needs_review | 12 | 12 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterface` | `transaction` |  | needs_review | 5467 | 5467 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfacecontainer` | `transaction` |  | needs_review | 26 | 26 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfaceidentifier` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfacemember` | `transaction` |  | needs_review | 165 | 165 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glintftemplatedetail` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_humancapitalbatch` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_humancapitalbatchitem` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_humancapitalpassedreport` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inbox` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inboxhistory` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_investee` | `transaction` |  | needs_review | 14 | 14 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_investmentcategory` | `transaction` |  | needs_review | 7 | 7 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_invoice` | `transaction` |  | needs_review | 22 | 22 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_journalblock` | `transaction` |  | needs_review | 312 | 312 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_journalcreation` | `transaction` |  | needs_review | 37 | 37 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_kurshistory` | `transaction` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mapreconcile` | `transaction` |  | needs_review | 52 | 52 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mapreconcileaccount` | `transaction` |  | needs_review | 107 | 107 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_marketer` | `transaction` |  | needs_review | 43 | 43 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiq` | `transaction` |  | needs_review | 15 | 15 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_parameterjournal` | `transaction` |  | needs_review | 65 | 65 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_parameterjournalitem` | `transaction` |  | needs_review | 205 | 205 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_pettycashid` | `transaction` |  | needs_review | 5 | 5 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_product` | `transaction` |  | needs_review | 139 | 139 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_productaccountid` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_producthierarchy` | `transaction` |  | needs_review | 116 | 116 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_projectsponsor` | `transaction` |  | needs_review | 27 | 27 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_projectsponsordisbursement` | `transaction` |  | needs_review | 11 | 11 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_propinsi` | `transaction` |  | needs_review | 37 | 37 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_reconcileaccountbalance` | `transaction` |  | needs_review | 7290 | 7290 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_registerkurs` | `transaction` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_sponsor` | `transaction` |  | needs_review | 68 | 68 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_test` | `transaction` |  | needs_review | 103 | 103 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_totalfund` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transaction` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionbatch` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionitem` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionnumber` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transhistoryofchanges` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transrecongenlog` | `transaction` |  | needs_review | 218745 | 218745 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_wakafcertificate` | `transaction` |  | needs_review | 51 | 51 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workarea` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workunit` | `transaction` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Views

| Nama | Schema | Catatan |
| --- | --- | --- |
| `account_off_bs` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `accountinstance_neraca` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `branch` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `branchlocation` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `branchlocation_oldtran` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `cashaccountall` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `debtor_all` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `donor` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `employee` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `marketer` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `userapp` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `vbatchupload` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `vdonor` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `vemployee` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `vemployeecashadvance` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `vproduct` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `vprogrampartner` | `transaction` | needs_review (definisi view lihat DDL sumber) |
| `zakahobject` | `transaction` | needs_review (definisi view lihat DDL sumber) |

## Tables

Daftar table:

- [`transaction.account`](#table-transaction-account) — 17 kolom
- [`transaction.accountdetail`](#table-transaction-accountdetail) — 2 kolom
- [`transaction.accountgroup`](#table-transaction-accountgroup) — 3 kolom
- [`transaction.accounthierarchy`](#table-transaction-accounthierarchy) — 3 kolom
- [`transaction.accountingday`](#table-transaction-accountingday) — 8 kolom
- [`transaction.accountingperiode`](#table-transaction-accountingperiode) — 9 kolom
- [`transaction.accountingyear`](#table-transaction-accountingyear) — 7 kolom
- [`transaction.accountinstance`](#table-transaction-accountinstance) — 20 kolom
- [`transaction.accountinterface`](#table-transaction-accountinterface) — 6 kolom
- [`transaction.accountinterfacemember`](#table-transaction-accountinterfacemember) — 3 kolom
- [`transaction.accountmanager`](#table-transaction-accountmanager) — 5 kolom
- [`transaction.accountreceivable`](#table-transaction-accountreceivable) — 7 kolom
- [`transaction.accounttransactionitem`](#table-transaction-accounttransactionitem) — 22 kolom
- [`transaction.accreceivabletransactitem`](#table-transaction-accreceivabletransactitem) — 5 kolom
- [`transaction.accsubsystem`](#table-transaction-accsubsystem) — 13 kolom
- [`transaction.amortizedcost`](#table-transaction-amortizedcost) — 4 kolom
- [`transaction.assetcategory`](#table-transaction-assetcategory) — 12 kolom
- [`transaction.balancesumgroup`](#table-transaction-balancesumgroup) — 3 kolom
- [`transaction.balancesumitem`](#table-transaction-balancesumitem) — 4 kolom
- [`transaction.balancesumitemmember`](#table-transaction-balancesumitemmember) — 3 kolom
- [`transaction.balancesumitemtrancode`](#table-transaction-balancesumitemtrancode) — 3 kolom
- [`transaction.bank`](#table-transaction-bank) — 3 kolom
- [`transaction.bankaccountlist`](#table-transaction-bankaccountlist) — 6 kolom
- [`transaction.batchupload`](#table-transaction-batchupload) — 12 kolom
- [`transaction.batchuploaditem`](#table-transaction-batchuploaditem) — 28 kolom
- [`transaction.blobregistration`](#table-transaction-blobregistration) — 3 kolom
- [`transaction.bpscenario`](#table-transaction-bpscenario) — 3 kolom
- [`transaction.bpscenariostep`](#table-transaction-bpscenariostep) — 5 kolom
- [`transaction.bpscript`](#table-transaction-bpscript) — 4 kolom
- [`transaction.branchlocation_old`](#table-transaction-branchlocation-old) — 7 kolom
- [`transaction.branchparameter`](#table-transaction-branchparameter) — 4 kolom
- [`transaction.bsz`](#table-transaction-bsz) — 4 kolom
- [`transaction.bszdetail`](#table-transaction-bszdetail) — 7 kolom
- [`transaction.bsztransaction`](#table-transaction-bsztransaction) — 3 kolom
- [`transaction.budget`](#table-transaction-budget) — 16 kolom
- [`transaction.budgetitem`](#table-transaction-budgetitem) — 10 kolom
- [`transaction.budgetitemhierarchy`](#table-transaction-budgetitemhierarchy) — 4 kolom
- [`transaction.budgetowner`](#table-transaction-budgetowner) — 7 kolom
- [`transaction.budgetownerhierarchy`](#table-transaction-budgetownerhierarchy) — 4 kolom
- [`transaction.budgetperiod`](#table-transaction-budgetperiod) — 5 kolom
- [`transaction.budgetrevision`](#table-transaction-budgetrevision) — 4 kolom
- [`transaction.budgettransaction`](#table-transaction-budgettransaction) — 4 kolom
- [`transaction.cashaccount`](#table-transaction-cashaccount) — 13 kolom
- [`transaction.cashadvancememoinfo`](#table-transaction-cashadvancememoinfo) — 3 kolom
- [`transaction.cashadvanceprograminfo`](#table-transaction-cashadvanceprograminfo) — 3 kolom
- [`transaction.cashadvancereturninfo`](#table-transaction-cashadvancereturninfo) — 5 kolom
- [`transaction.cashflowgroup`](#table-transaction-cashflowgroup) — 9 kolom
- [`transaction.cashflowmember`](#table-transaction-cashflowmember) — 9 kolom
- [`transaction.coa_convertion`](#table-transaction-coa-convertion) — 2 kolom
- [`transaction.corporatedonor`](#table-transaction-corporatedonor) — 14 kolom
- [`transaction.costpaidinadvance`](#table-transaction-costpaidinadvance) — 6 kolom
- [`transaction.cpalpamapping`](#table-transaction-cpalpamapping) — 3 kolom
- [`transaction.currency`](#table-transaction-currency) — 30 kolom
- [`transaction.currency_pkpu`](#table-transaction-currency-pkpu) — 30 kolom
- [`transaction.custom_idgen`](#table-transaction-custom-idgen) — 4 kolom
- [`transaction.cutoff_dba_2017`](#table-transaction-cutoff-dba-2017) — 2 kolom
- [`transaction.cutoff_dba_2021`](#table-transaction-cutoff-dba-2021) — 2 kolom
- [`transaction.cutoff_dba_detail_2017`](#table-transaction-cutoff-dba-detail-2017) — 20 kolom
- [`transaction.cutoff_dba_detail_2021`](#table-transaction-cutoff-dba-detail-2021) — 20 kolom
- [`transaction.cutoff_trxitem_sum_2017`](#table-transaction-cutoff-trxitem-sum-2017) — 7 kolom
- [`transaction.daemons`](#table-transaction-daemons) — 2 kolom
- [`transaction.dailybalance`](#table-transaction-dailybalance) — 20 kolom
- [`transaction.dailybalancecash`](#table-transaction-dailybalancecash) — 20 kolom
- [`transaction.dailyprojectbalance`](#table-transaction-dailyprojectbalance) — 21 kolom
- [`transaction.depreciableasset`](#table-transaction-depreciableasset) — 15 kolom
- [`transaction.dinarcertificate`](#table-transaction-dinarcertificate) — 5 kolom
- [`transaction.dinarholder`](#table-transaction-dinarholder) — 2 kolom
- [`transaction.distributiontransferinfo`](#table-transaction-distributiontransferinfo) — 9 kolom
- [`transaction.distributiontransferinfotemp`](#table-transaction-distributiontransferinfotemp) — 9 kolom
- [`transaction.donorbankaccount`](#table-transaction-donorbankaccount) — 2 kolom
- [`transaction.donorcommitment`](#table-transaction-donorcommitment) — 4 kolom
- [`transaction.donortotalfund`](#table-transaction-donortotalfund) — 4 kolom
- [`transaction.enum_int`](#table-transaction-enum-int) — 3 kolom
- [`transaction.enum_varchar`](#table-transaction-enum-varchar) — 3 kolom
- [`transaction.externaldebtor`](#table-transaction-externaldebtor) — 7 kolom
- [`transaction.externaltransaction`](#table-transaction-externaltransaction) — 3 kolom
- [`transaction.fact_daily_balance`](#table-transaction-fact-daily-balance) — 9 kolom
- [`transaction.fieldofwork`](#table-transaction-fieldofwork) — 4 kolom
- [`transaction.financialaccount`](#table-transaction-financialaccount) — 12 kolom
- [`transaction.fixedasset`](#table-transaction-fixedasset) — 6 kolom
- [`transaction.fixedassettransactinfo`](#table-transaction-fixedassettransactinfo) — 4 kolom
- [`transaction.fixedassettransactitem`](#table-transaction-fixedassettransactitem) — 3 kolom
- [`transaction.funddailybalance`](#table-transaction-funddailybalance) — 9 kolom
- [`transaction.fundproject`](#table-transaction-fundproject) — 4 kolom
- [`transaction.fundprojectaccount`](#table-transaction-fundprojectaccount) — 4 kolom
- [`transaction.fundprojectsponsor`](#table-transaction-fundprojectsponsor) — 9 kolom
- [`transaction.gammu`](#table-transaction-gammu) — 1 kolom
- [`transaction.generalclass`](#table-transaction-generalclass) — 1 kolom
- [`transaction.generatejournal_candidate`](#table-transaction-generatejournal-candidate) — 1 kolom
- [`transaction.glinterface`](#table-transaction-glinterface) — 6 kolom
- [`transaction.glinterfacecontainer`](#table-transaction-glinterfacecontainer) — 3 kolom
- [`transaction.glinterfaceidentifier`](#table-transaction-glinterfaceidentifier) — 8 kolom
- [`transaction.glinterfacemember`](#table-transaction-glinterfacemember) — 6 kolom
- [`transaction.glintftemplate`](#table-transaction-glintftemplate) — 3 kolom
- [`transaction.glintftemplatedetail`](#table-transaction-glintftemplatedetail) — 5 kolom
- [`transaction.globalglinterface`](#table-transaction-globalglinterface) — 3 kolom
- [`transaction.hi_permil`](#table-transaction-hi-permil) — 8 kolom
- [`transaction.hipermildistribution`](#table-transaction-hipermildistribution) — 4 kolom
- [`transaction.historyofchanges`](#table-transaction-historyofchanges) — 10 kolom
- [`transaction.humancapitalbatch`](#table-transaction-humancapitalbatch) — 6 kolom
- [`transaction.humancapitalbatchitem`](#table-transaction-humancapitalbatchitem) — 27 kolom
- [`transaction.humancapitalpassedreport`](#table-transaction-humancapitalpassedreport) — 4 kolom
- [`transaction.id_gen`](#table-transaction-id-gen) — 3 kolom
- [`transaction.inbox`](#table-transaction-inbox) — 10 kolom
- [`transaction.inboxhistory`](#table-transaction-inboxhistory) — 7 kolom
- [`transaction.inboxtransaction`](#table-transaction-inboxtransaction) — 2 kolom
- [`transaction.individualdonor`](#table-transaction-individualdonor) — 33 kolom
- [`transaction.intrnewtransaction`](#table-transaction-intrnewtransaction) — 5 kolom
- [`transaction.intrpicktransaction`](#table-transaction-intrpicktransaction) — 3 kolom
- [`transaction.inventory`](#table-transaction-inventory) — 6 kolom
- [`transaction.inventorycategory`](#table-transaction-inventorycategory) — 5 kolom
- [`transaction.investee`](#table-transaction-investee) — 8 kolom
- [`transaction.investment`](#table-transaction-investment) — 14 kolom
- [`transaction.investmentcategory`](#table-transaction-investmentcategory) — 5 kolom
- [`transaction.investmentmanager`](#table-transaction-investmentmanager) — 4 kolom
- [`transaction.invoice`](#table-transaction-invoice) — 10 kolom
- [`transaction.invoicefa`](#table-transaction-invoicefa) — 2 kolom
- [`transaction.invoiceproduct`](#table-transaction-invoiceproduct) — 12 kolom
- [`transaction.invoiceproductdefaultdata`](#table-transaction-invoiceproductdefaultdata) — 8 kolom
- [`transaction.jenis_dana`](#table-transaction-jenis-dana) — 2 kolom
- [`transaction.jenisrak`](#table-transaction-jenisrak) — 4 kolom
- [`transaction.journal`](#table-transaction-journal) — 28 kolom
- [`transaction.journal_bck`](#table-transaction-journal-bck) — 28 kolom
- [`transaction.journal_bck20150821`](#table-transaction-journal-bck20150821) — 28 kolom
- [`transaction.journal_cashflow`](#table-transaction-journal-cashflow) — 2 kolom
- [`transaction.journal_cashflow_candidate`](#table-transaction-journal-cashflow-candidate) — 1 kolom
- [`transaction.journalblock`](#table-transaction-journalblock) — 9 kolom
- [`transaction.journalcode`](#table-transaction-journalcode) — 8 kolom
- [`transaction.journaldeletion`](#table-transaction-journaldeletion) — 4 kolom
- [`transaction.journalitem`](#table-transaction-journalitem) — 36 kolom
- [`transaction.journalitem_cashflow`](#table-transaction-journalitem-cashflow) — 3 kolom
- [`transaction.kota_kabupaten`](#table-transaction-kota-kabupaten) — 4 kolom
- [`transaction.kurshistory`](#table-transaction-kurshistory) — 18 kolom
- [`transaction.mapaccount`](#table-transaction-mapaccount) — 2 kolom
- [`transaction.mapping_gldetail_2014`](#table-transaction-mapping-gldetail-2014) — 2 kolom
- [`transaction.mapping_glint_asset`](#table-transaction-mapping-glint-asset) — 2 kolom
- [`transaction.mapping_glinttemplate_2014`](#table-transaction-mapping-glinttemplate-2014) — 2 kolom
- [`transaction.mappingcoa`](#table-transaction-mappingcoa) — 2 kolom
- [`transaction.mapreconcile`](#table-transaction-mapreconcile) — 10 kolom
- [`transaction.mapreconcileaccount`](#table-transaction-mapreconcileaccount) — 3 kolom
- [`transaction.masterkurs`](#table-transaction-masterkurs) — 5 kolom
- [`transaction.mustahiq`](#table-transaction-mustahiq) — 13 kolom
- [`transaction.mustahiqbankaccount`](#table-transaction-mustahiqbankaccount) — 2 kolom
- [`transaction.mustahiqcorporate`](#table-transaction-mustahiqcorporate) — 4 kolom
- [`transaction.mustahiqpersonal`](#table-transaction-mustahiqpersonal) — 13 kolom
- [`transaction.negara`](#table-transaction-negara) — 2 kolom
- [`transaction.parameter`](#table-transaction-parameter) — 5 kolom
- [`transaction.parameterglobal`](#table-transaction-parameterglobal) — 9 kolom
- [`transaction.parameterglobaltes`](#table-transaction-parameterglobaltes) — 9 kolom
- [`transaction.parameterinbox`](#table-transaction-parameterinbox) — 4 kolom
- [`transaction.parameterjournal`](#table-transaction-parameterjournal) — 4 kolom
- [`transaction.parameterjournalitem`](#table-transaction-parameterjournalitem) — 12 kolom
- [`transaction.periodebalance`](#table-transaction-periodebalance) — 18 kolom
- [`transaction.periodeprojectbalance`](#table-transaction-periodeprojectbalance) — 19 kolom
- [`transaction.product`](#table-transaction-product) — 24 kolom
- [`transaction.productaccount`](#table-transaction-productaccount) — 9 kolom
- [`transaction.producthierarchy`](#table-transaction-producthierarchy) — 4 kolom
- [`transaction.project`](#table-transaction-project) — 8 kolom
- [`transaction.projectsponsordisbursement`](#table-transaction-projectsponsordisbursement) — 7 kolom
- [`transaction.propinsi`](#table-transaction-propinsi) — 4 kolom
- [`transaction.prospectivedonor`](#table-transaction-prospectivedonor) — 4 kolom
- [`transaction.rakcabang`](#table-transaction-rakcabang) — 4 kolom
- [`transaction.rakpusat`](#table-transaction-rakpusat) — 3 kolom
- [`transaction.reconcileaccountbalance`](#table-transaction-reconcileaccountbalance) — 4 kolom
- [`transaction.reconciletransaction`](#table-transaction-reconciletransaction) — 17 kolom
- [`transaction.reconciletransactionbck`](#table-transaction-reconciletransactionbck) — 14 kolom
- [`transaction.registerkurs`](#table-transaction-registerkurs) — 17 kolom
- [`transaction.rekeningbmm`](#table-transaction-rekeningbmm) — 1 kolom
- [`transaction.revaluationhistory`](#table-transaction-revaluationhistory) — 6 kolom
- [`transaction.reversetransaction`](#table-transaction-reversetransaction) — 2 kolom
- [`transaction.rpvaccount`](#table-transaction-rpvaccount) — 4 kolom
- [`transaction.rpvaccountdetail`](#table-transaction-rpvaccountdetail) — 6 kolom
- [`transaction.salestransaction`](#table-transaction-salestransaction) — 2 kolom
- [`transaction.script_collection`](#table-transaction-script-collection) — 4 kolom
- [`transaction.sessionblob`](#table-transaction-sessionblob) — 4 kolom
- [`transaction.sim_logrun`](#table-transaction-sim-logrun) — 6 kolom
- [`transaction.snapshot_accountinstance`](#table-transaction-snapshot-accountinstance) — 21 kolom
- [`transaction.sponsor`](#table-transaction-sponsor) — 6 kolom
- [`transaction.sponsortransaction`](#table-transaction-sponsortransaction) — 7 kolom
- [`transaction.subsysteminteraction`](#table-transaction-subsysteminteraction) — 7 kolom
- [`transaction.tempcandidatejournal`](#table-transaction-tempcandidatejournal) — 11 kolom
- [`transaction.temptable`](#table-transaction-temptable) — 7 kolom
- [`transaction.temptable_ori`](#table-transaction-temptable-ori) — 7 kolom
- [`transaction.temptabledata`](#table-transaction-temptabledata) — 7 kolom
- [`transaction.temptablenew`](#table-transaction-temptablenew) — 7 kolom
- [`transaction.tmp_accounttransactionitem_bck`](#table-transaction-tmp-accounttransactionitem-bck) — 22 kolom
- [`transaction.tmp_acctranitem_repair_zakat2`](#table-transaction-tmp-acctranitem-repair-zakat2) — 22 kolom
- [`transaction.tmp_deletedaccount`](#table-transaction-tmp-deletedaccount) — 1 kolom
- [`transaction.tmp_gen_productaccount`](#table-transaction-tmp-gen-productaccount) — 4 kolom
- [`transaction.tmp_hctransactiongroup`](#table-transaction-tmp-hctransactiongroup) — 9 kolom
- [`transaction.tmp_journalitem_bck`](#table-transaction-tmp-journalitem-bck) — 36 kolom
- [`transaction.tmp_mapping_repair_zakat`](#table-transaction-tmp-mapping-repair-zakat) — 10 kolom
- [`transaction.tmp_mappingproduct1`](#table-transaction-tmp-mappingproduct1) — 14 kolom
- [`transaction.tmp_mappingtran_accountcode`](#table-transaction-tmp-mappingtran-accountcode) — 2 kolom
- [`transaction.tmp_mappingtran_accountcode2`](#table-transaction-tmp-mappingtran-accountcode2) — 2 kolom
- [`transaction.tmp_newprogramname`](#table-transaction-tmp-newprogramname) — 3 kolom
- [`transaction.tmp_program`](#table-transaction-tmp-program) — 10 kolom
- [`transaction.tmp_repair_journalamil`](#table-transaction-tmp-repair-journalamil) — 1 kolom
- [`transaction.tmp_repair_phpinfaq`](#table-transaction-tmp-repair-phpinfaq) — 4 kolom
- [`transaction.tmp_repair_porsiamilinfaq`](#table-transaction-tmp-repair-porsiamilinfaq) — 3 kolom
- [`transaction.tmp_tranitem_repair_zakat2`](#table-transaction-tmp-tranitem-repair-zakat2) — 17 kolom
- [`transaction.tmp_tranitem_repair_zakat_bck1`](#table-transaction-tmp-tranitem-repair-zakat-bck1) — 17 kolom
- [`transaction.tmp_transactiongroup`](#table-transaction-tmp-transactiongroup) — 10 kolom
- [`transaction.tmp_transactionitem_bck`](#table-transaction-tmp-transactionitem-bck) — 17 kolom
- [`transaction.transaction`](#table-transaction-transaction) — 36 kolom
- [`transaction.transactionbatch`](#table-transaction-transactionbatch) — 9 kolom
- [`transaction.transactionitem`](#table-transaction-transactionitem) — 17 kolom
- [`transaction.transactionitem_inject`](#table-transaction-transactionitem-inject) — 17 kolom
- [`transaction.transactiontype`](#table-transaction-transactiontype) — 3 kolom
- [`transaction.transaksirak`](#table-transaction-transaksirak) — 12 kolom
- [`transaction.transhistoryofchanges`](#table-transaction-transhistoryofchanges) — 7 kolom
- [`transaction.transitemglinterface`](#table-transaction-transitemglinterface) — 4 kolom
- [`transaction.transrecongenlog`](#table-transaction-transrecongenlog) — 3 kolom
- [`transaction.userapp_`](#table-transaction-userapp-) — 9 kolom
- [`transaction.userapp_old`](#table-transaction-userapp-old) — 9 kolom
- [`transaction.usergroup`](#table-transaction-usergroup) — 5 kolom
- [`transaction.usergroup_`](#table-transaction-usergroup-) — 5 kolom
- [`transaction.usergroupapp`](#table-transaction-usergroupapp) — 2 kolom
- [`transaction.usergroupapp_`](#table-transaction-usergroupapp-) — 2 kolom
- [`transaction.vendor`](#table-transaction-vendor) — 5 kolom
- [`transaction.volunteer`](#table-transaction-volunteer) — 8 kolom
- [`transaction.volunteertransaction`](#table-transaction-volunteertransaction) — 2 kolom
- [`transaction.wakafcertificate`](#table-transaction-wakafcertificate) — 6 kolom
- [`transaction.workarea`](#table-transaction-workarea) — 3 kolom
- [`transaction.workunit`](#table-transaction-workunit) — 3 kolom

### Table `transaction.account` <a id="table-transaction-account"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `account` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_name` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `account_level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `is_detail` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `account_type` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `is_system` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userid_last_modified` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `time_last_modified` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fl_parent_account` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `userid_create` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `time_create` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `fl_cpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `fl_lpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `isactivaoffbalancesheet` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `isrpvrakreportshow` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `isrpvaccount` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code)` |  |

### Table `transaction.accountdetail` <a id="table-transaction-accountdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountdetail` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_account` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_detail_account` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fl_account, fl_detail_account)` |  |

### Table `transaction.accountgroup` <a id="table-transaction-accountgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountgroup` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountgroup_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountgroup_name` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `transaction.accounthierarchy` <a id="table-transaction-accounthierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accounthierarchy` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounthierarchy_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_parentaccountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_childaccountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accounthierarchy_id)` |  |

### Table `transaction.accountingday` <a id="table-transaction-accountingday"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountingday` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `periode_status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `islastperiod` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `periode_code` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `fl_accountingperiode` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 6 | `fl_accountingyear` | `character varying(4)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 7 | `datevalue` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isworkday` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periode_code, fl_accountingperiode, fl_accountingyear)` |  |

### Table `transaction.accountingperiode` <a id="table-transaction-accountingperiode"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountingperiode` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_accountingyear` | `character varying(4)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `periode_code` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `periode_status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_lastyearperiode` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `pcode_accday_end` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `pcode_accday_start` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fl_accountingperiode_start` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fl_accountingyear_start` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fl_accountingyear, periode_code)` |  |

### Table `transaction.accountingyear` <a id="table-transaction-accountingyear"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountingyear` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periode_code` | `character varying(4)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `periode_status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fl_current_periode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `pcode_accper_end` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `pcode_accper_start` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fl_accountingyear_start` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periode_code)` |  |

### Table `transaction.accountinstance` <a id="table-transaction-accountinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountinstance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_cpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fl_lpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isbolehinput` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periodebalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `balance_sign` | `numeric(1,0)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountinstance_id)` |  |

### Table `transaction.accountinterface` <a id="table-transaction-accountinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountinterface` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interface_code` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `interface_type` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_active` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (interface_code)` |  |

### Table `transaction.accountinterfacemember` <a id="table-transaction-accountinterfacemember"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountinterfacemember` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `member_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `interface_code` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (member_id)` |  |

### Table `transaction.accountmanager` <a id="table-transaction-accountmanager"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountmanager` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `amcode` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `rcno` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `employeename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (amcode)` |  |

### Table `transaction.accountreceivable` <a id="table-transaction-accountreceivable"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accountreceivable` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `accountreceivabletype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `employeeidnumber` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `externaldebtorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `debtorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `partnerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.accounttransactionitem` <a id="table-transaction-accounttransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accounttransactionitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounttitype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `amountperunit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `totalunit` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `ashnaf` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `percentageofamil` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `distributionitemaccount` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `cattype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `returntransactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `catransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `isupdatebalance` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `distributiontransferid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kota` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `kecamatan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `distributioncategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `fundaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.accreceivabletransactitem` <a id="table-transaction-accreceivabletransactitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accreceivabletransactitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `artransactitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `investmenttitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `principalamount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `shareamount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.accsubsystem` <a id="table-transaction-accsubsystem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `accsubsystem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsystemcode` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `titlesubsystem` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `servername` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `username` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `password` | `character varying(30)` | YES | NULL::character varying |  | YES | full | synthetic_only | YES | needs_review |
| 7 | `createjournalscriptid` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `sessionname` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `usecurrentlogin` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `authjournalscriptid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `applicationid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `oldstylescripting` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsystemcode)` |  |

### Table `transaction.amortizedcost` <a id="table-transaction-amortizedcost"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `amortizedcost` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `amortizedcosttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `costaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.assetcategory` <a id="table-transaction-assetcategory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `assetcategory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `assetcategoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentassetcategoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `assetcategoryname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `assetcategorycode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `thresholdvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `defaultlifetime` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputer` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `inputtime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `isdepreciable` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `assettype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (assetcategoryid)` |  |

### Table `transaction.balancesumgroup` <a id="table-transaction-balancesumgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `balancesumgroup` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `groupcode` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `groupname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `groupdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (groupcode)` |  |

### Table `transaction.balancesumitem` <a id="table-transaction-balancesumitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `balancesumitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `itemcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `itemname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `groupcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `transaction.balancesumitemmember` <a id="table-transaction-balancesumitemmember"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `balancesumitemmember` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `memberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `itemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (memberid)` |  |

### Table `transaction.balancesumitemtrancode` <a id="table-transaction-balancesumitemtrancode"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `balancesumitemtrancode` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `memberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `itemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (memberid)` |  |

### Table `transaction.bank` <a id="table-transaction-bank"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bank` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankcode` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankshortname` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankname` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankcode)` |  |

### Table `transaction.bankaccountlist` <a id="table-transaction-bankaccountlist"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bankaccountlist` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankaccountname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `bankaccountlisttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `bankcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isdefault` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `transaction.batchupload` <a id="table-transaction-batchupload"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `batchupload` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `batchid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `uploaduser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `uploaddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `totalamount` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `batchuploadtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `authorizeduser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `totalrecord` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `filename` | `character varying(400)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (batchid)` |  |

### Table `transaction.batchuploaditem` <a id="table-transaction-batchuploaditem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `batchuploaditem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `batchitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `authstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `validationstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `donornamefromdesc` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `iscreatenewdonor` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `bankaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 17 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 18 | `amountzakatprofesi` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `amountzakatmaal` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `amountzakatfitrah` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `amountinfaq` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `amountdpu` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `amountanakyatim` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `amountanakasuh` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `amounttitipanwakaf` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `amountqurban` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `amountnonhalal` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `amountfidyah` | `numeric(30,6)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (batchitemid)` |  |

### Table `transaction.blobregistration` <a id="table-transaction-blobregistration"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `blobregistration` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `actualfilename` | `character varying(128)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `istemporary` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `transaction.bpscenario` <a id="table-transaction-bpscenario"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bpscenario` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bpscenarioid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bpscenariocode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bpscenarioname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bpscenarioid)` |  |

### Table `transaction.bpscenariostep` <a id="table-transaction-bpscenariostep"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bpscenariostep` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bpstepid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bpstepsequence` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bpscriptid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `bpscenarioid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isenabled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bpstepid)` |  |

### Table `transaction.bpscript` <a id="table-transaction-bpscript"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bpscript` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bpscriptid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bpscriptdescription` | `character varying(250)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bpscriptname` | `character varying(250)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `bpscriptpath` | `character varying(250)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bpscriptid)` |  |

### Table `transaction.branchlocation_old` <a id="table-transaction-branchlocation-old"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `branchlocation_old` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branch_code` | `character varying(5)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `masterbranch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dataid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.branchparameter` <a id="table-transaction-branchparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `branchparameter` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branchcode` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `inputer` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `printertype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `voucherformat` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branchcode)` |  |

### Table `transaction.bsz` <a id="table-transaction-bsz"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bsz` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bszid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bsznumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `bszdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bszid)` |  |

### Table `transaction.bszdetail` <a id="table-transaction-bszdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bszdetail` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bszdetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bszid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `item` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `percentage` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `year` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `basicvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `zakahvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bszdetailid)` |  |

### Table `transaction.bsztransaction` <a id="table-transaction-bsztransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `bsztransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bszid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionitemid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bsztransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bsztransactionid)` |  |

### Table `transaction.budget` <a id="table-transaction-budget"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budget` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `budgetid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `periodid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ownerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `itemcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `realization` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `revisionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `budgetcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `parentbudgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `budgettype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `itemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (budgetid)` |  |

### Table `transaction.budgetitem` <a id="table-transaction-budgetitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgetitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `budgetitemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `budgetitemdescription` | `character varying(250)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ownerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parentbudgetitemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `is_detail` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 8 | `budgetitemname` | `character varying(200)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `parentitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `transaction.budgetitemhierarchy` <a id="table-transaction-budgetitemhierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgetitemhierarchy` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `hierarchyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `childitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (hierarchyid)` |  |

### Table `transaction.budgetowner` <a id="table-transaction-budgetowner"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgetowner` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `ownerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `ownername` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentownerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_detail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `ownercode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ownerid)` |  |

### Table `transaction.budgetownerhierarchy` <a id="table-transaction-budgetownerhierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgetownerhierarchy` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `hierarchyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentownerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `childownerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (hierarchyid)` |  |

### Table `transaction.budgetperiod` <a id="table-transaction-budgetperiod"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgetperiod` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentperiodid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `periodvalue` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isopen` | `character varying(1)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `periodname` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periodid)` |  |

### Table `transaction.budgetrevision` <a id="table-transaction-budgetrevision"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgetrevision` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `revisionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `budgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (revisionid)` |  |

### Table `transaction.budgettransaction` <a id="table-transaction-budgettransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `budgettransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `budgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `budgettranstype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.cashaccount` <a id="table-transaction-cashaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cashaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankname` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankaccountno` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `accountcurrency` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cashaccounttype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `username` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `accountno` | `character varying(30)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 7 | `bankcode` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `accountinterface` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `cashcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isamilaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `isreconaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.cashadvancememoinfo` <a id="table-transaction-cashadvancememoinfo"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cashadvancememoinfo` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realmemoid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `transaction.cashadvanceprograminfo` <a id="table-transaction-cashadvanceprograminfo"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cashadvanceprograminfo` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `sourcetransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reporttransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (sourcetransactionid, reporttransactionid)` |  |

### Table `transaction.cashadvancereturninfo` <a id="table-transaction-cashadvancereturninfo"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cashadvancereturninfo` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `sourcetransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `returntransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `returnamount` | `numeric(20,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `reimburseamount` | `numeric(20,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (sourcetransactionid)` |  |

### Table `transaction.cashflowgroup` <a id="table-transaction-cashflowgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cashflowgroup` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cfgroupid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cfgroupcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cfgroupname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cfgroupdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `cfsequencenumber` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cfparentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `cfgrouplevel` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `cfoperationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (cfgroupid)` |  |

### Table `transaction.cashflowmember` <a id="table-transaction-cashflowmember"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cashflowmember` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cfmemberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cfgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `trancodeexclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `trancodeinclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `journalcodeexclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `journalcodeinclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `additionalinfo` | `character varying(300)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (cfmemberid)` |  |

### Table `transaction.coa_convertion` <a id="table-transaction-coa-convertion"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `coa_convertion` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode_old` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode_new` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountcode_old)` |  |

### Table `transaction.corporatedonor` <a id="table-transaction-corporatedonor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `corporatedonor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `corporation` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `siupp` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `tdp` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locationtype` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `ownertype` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `establisheddate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `establishedplace` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `contactperson` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `patronagecompany` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 11 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `cpemail` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `cpphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `cpmobilenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `transaction.costpaidinadvance` <a id="table-transaction-costpaidinadvance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `costpaidinadvance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `hascontract` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `contractbegindate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `contractduration` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `contractenddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `contractno` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.cpalpamapping` <a id="table-transaction-cpalpamapping"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cpalpamapping` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_lpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_cpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cpalpamapping_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (cpalpamapping_id)` |  |

### Table `transaction.currency` <a id="table-transaction-currency"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `currency` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `currency_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(64)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currentvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdefault` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isstandard` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `centralbank_currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `short_name` | `character varying(10)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `full_name` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `country_owner` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_beli_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kurs_jual_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `tanggal_limit` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `terminal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `tanggal_otorisasi` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `deviasi_maksimal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `symbol` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `symbol_says` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code)` |  |

### Table `transaction.currency_pkpu` <a id="table-transaction-currency-pkpu"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `currency_pkpu` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `currency_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(64)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currentvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdefault` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isstandard` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `centralbank_currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `short_name` | `character varying(10)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `full_name` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `country_owner` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_beli_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kurs_jual_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `tanggal_limit` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `terminal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `tanggal_otorisasi` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `deviasi_maksimal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `symbol` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `symbol_says` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code)` |  |

### Table `transaction.custom_idgen` <a id="table-transaction-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `custom_idgen` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idname` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idcode` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locked` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idname, idcode)` |  |

### Table `transaction.cutoff_dba_2017` <a id="table-transaction-cutoff-dba-2017"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cutoff_dba_2017` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `max_period` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.cutoff_dba_2021` <a id="table-transaction-cutoff-dba-2021"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cutoff_dba_2021` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `max_period` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.cutoff_dba_detail_2017` <a id="table-transaction-cutoff-dba-detail-2017"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cutoff_dba_detail_2017` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `datevalue` | `date` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingyear` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.cutoff_dba_detail_2021` <a id="table-transaction-cutoff-dba-detail-2021"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cutoff_dba_detail_2021` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `datevalue` | `date` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingyear` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.cutoff_trxitem_sum_2017` <a id="table-transaction-cutoff-trxitem-sum-2017"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `cutoff_trxitem_sum_2017` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `amount` | `numeric` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `count_amount` | `bigint` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.daemons` <a id="table-transaction-daemons"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `daemons` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Start` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `Info` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.dailybalance` <a id="table-transaction-dailybalance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `dailybalance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `datevalue` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dailybalance_id)` |  |

### Table `transaction.dailybalancecash` <a id="table-transaction-dailybalancecash"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `dailybalancecash` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `datevalue` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dailybalance_id)` |  |

### Table `transaction.dailyprojectbalance` <a id="table-transaction-dailyprojectbalance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `dailyprojectbalance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailyprojectbalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `datevalue` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dailyprojectbalance_id)` |  |

### Table `transaction.depreciableasset` <a id="table-transaction-depreciableasset"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `depreciableasset` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `accountnoproduct` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `depreciableassettype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `lifetime` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nilaiawal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilaisisa` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `penyusutanke` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tanggalakhirpenyusutan` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `tanggalperolehan` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `tanggalprosesberikut` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `tanggalprosesterakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `totalpenyusutan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `nominalpenyusutan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `deprstate` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.dinarcertificate` <a id="table-transaction-dinarcertificate"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `dinarcertificate` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dinarcertificateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `dinarcertificatenumber` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `certificatedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dinarcertificateid)` |  |

### Table `transaction.dinarholder` <a id="table-transaction-dinarholder"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `dinarholder` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.distributiontransferinfo` <a id="table-transaction-distributiontransferinfo"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `distributiontransferinfo` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `distributionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `reporttransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `branchdestination` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branchsource` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `reportstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branchreporttransid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `branchreportstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (distributionid)` |  |

### Table `transaction.distributiontransferinfotemp` <a id="table-transaction-distributiontransferinfotemp"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `distributiontransferinfotemp` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `distributionid` | `bigint` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `reporttransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `branchdestination` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branchsource` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `reportstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branchreporttransid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `branchreportstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.donorbankaccount` <a id="table-transaction-donorbankaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `donorbankaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `transaction.donorcommitment` <a id="table-transaction-donorcommitment"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `donorcommitment` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `commitmentid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `commitmentamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (commitmentid)` |  |

### Table `transaction.donortotalfund` <a id="table-transaction-donortotalfund"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `donortotalfund` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `totalfundid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `totalamount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (totalfundid)` |  |

### Table `transaction.enum_int` <a id="table-transaction-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `enum_int` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `transaction.enum_varchar` <a id="table-transaction-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `enum_varchar` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `character varying(3)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `transaction.externaldebtor` <a id="table-transaction-externaldebtor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `externaldebtor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `debtorid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `debtorname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `debtorcode` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `debtoraddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `debtorphone` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (debtorid)` |  |

### Table `transaction.externaltransaction` <a id="table-transaction-externaltransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `externaltransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `exttransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (exttransactionid)` |  |

### Table `transaction.fact_daily_balance` <a id="table-transaction-fact-daily-balance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fact_daily_balance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fact_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fact_date` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fact_date_fmt` | `character varying(8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `currency_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `balance_ekiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fact_id)` |  |

### Table `transaction.fieldofwork` <a id="table-transaction-fieldofwork"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fieldofwork` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fworkcode` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fworkname` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fnpwzcode` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fworkid)` |  |

### Table `transaction.financialaccount` <a id="table-transaction-financialaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `financialaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `accountname` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `currencycode` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `financialaccounttype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `openingdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountcode` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastdailybalanceid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balancedeposit` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.fixedasset` <a id="table-transaction-fixedasset"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fixedasset` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `totaldibayar` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `qty` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `assetcategoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `uangmuka` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `hargajual` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.fixedassettransactinfo` <a id="table-transaction-fixedassettransactinfo"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fixedassettransactinfo` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `cashadvance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `sellamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.fixedassettransactitem` <a id="table-transaction-fixedassettransactitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fixedassettransactitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cashadvance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sellamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.funddailybalance` <a id="table-transaction-funddailybalance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `funddailybalance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalanceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balancedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `trialbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isclosed` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountno` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dailybalanceid)` |  |

### Table `transaction.fundproject` <a id="table-transaction-fundproject"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fundproject` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `budgetamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `startdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `finsihdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `transaction.fundprojectaccount` <a id="table-transaction-fundprojectaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fundprojectaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `startdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `finishdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `budgetamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.fundprojectsponsor` <a id="table-transaction-fundprojectsponsor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `fundprojectsponsor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `projectsponsorid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `projectsponsorcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `agreementdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `donationamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `disbursedamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `distributedamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (projectsponsorid)` |  |

### Table `transaction.gammu` <a id="table-transaction-gammu"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `gammu` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Version` | `smallint` | NO | (0)::smallint |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.generalclass` <a id="table-transaction-generalclass"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `generalclass` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `transaction.generatejournal_candidate` <a id="table-transaction-generatejournal-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `generatejournal_candidate` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `transaction.glinterface` <a id="table-transaction-glinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `glinterface` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interfaceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `interfacecode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (interfaceid)` |  |

### Table `transaction.glinterfacecontainer` <a id="table-transaction-glinterfacecontainer"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `glinterfacecontainer` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glicontainerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `glicontainercode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `glicontainername` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glicontainerid)` |  |

### Table `transaction.glinterfaceidentifier` <a id="table-transaction-glinterfaceidentifier"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `glinterfaceidentifier` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `identifier_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `programcategory` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `programtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `interfacecode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `interfacetype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (identifier_id)` |  |

### Table `transaction.glinterfacemember` <a id="table-transaction-glinterfacemember"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `glinterfacemember` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glimemberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `glimembercode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glimemberid)` |  |

### Table `transaction.glintftemplate` <a id="table-transaction-glintftemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `glintftemplate` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `template_code` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (template_code)` |  |

### Table `transaction.glintftemplatedetail` <a id="table-transaction-glintftemplatedetail"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `glintftemplatedetail` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `templatedetail_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `template_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `interfacecode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (templatedetail_id)` |  |

### Table `transaction.globalglinterface` <a id="table-transaction-globalglinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `globalglinterface` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glinterfacecode` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `glinterfacename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glinterfacecode)` |  |

### Table `transaction.hi_permil` <a id="table-transaction-hi-permil"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `hi_permil` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `p_year` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `p_month` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currency_code` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `day_number` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `process_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `id_hipermil` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 8 | `ekuiv_rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_hipermil)` |  |

### Table `transaction.hipermildistribution` <a id="table-transaction-hipermildistribution"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `hipermildistribution` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `distribution_id` | `character varying(2)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `hipermil_ratio` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ekuiv_rate_ratio` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id_hipermil` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (distribution_id, id_hipermil)` |  |

### Table `transaction.historyofchanges` <a id="table-transaction-historyofchanges"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `historyofchanges` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `historyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `changetype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `domainofchange` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `processtime` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `datasourcetype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `datasourceref` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `datasourceclass` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `datasourcerefinteger` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `terminalid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (historyid)` |  |

### Table `transaction.humancapitalbatch` <a id="table-transaction-humancapitalbatch"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `humancapitalbatch` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `batchid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `batchperioddesc` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `uploaddate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `uploaduserid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (batchid)` |  |

### Table `transaction.humancapitalbatchitem` <a id="table-transaction-humancapitalbatchitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `humancapitalbatchitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `batchitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `businessareacode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `businessareadescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `employeenumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `name` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `birthdate` | `timestamp without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `birthplace` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `gender` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `maritalstatus` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `position` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `organizationalunit` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `amountzakat` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `amountinfaq` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `amountanakyatim` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `amountanakasuh` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `iscreateemployeedata` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `organizationunit` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 22 | `workareaname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `mobilephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 24 | `amountwakaf` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `amountqurban` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `smslog_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `smslog_time` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (batchitemid)` |  |

### Table `transaction.humancapitalpassedreport` <a id="table-transaction-humancapitalpassedreport"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `humancapitalpassedreport` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `reportid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeenumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (reportid)` |  |

### Table `transaction.id_gen` <a id="table-transaction-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `id_gen` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_code` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `locked` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_code)` |  |

### Table `transaction.inbox` <a id="table-transaction-inbox"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `inbox` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `inboxid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `inputtime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `kodeinbox` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `filename` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `lastinboxhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `inboxtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inboxid)` |  |

### Table `transaction.inboxhistory` <a id="table-transaction-inboxhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `inboxhistory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `inboxhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `inboxid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `inputtime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `filename` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nextinboxhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inboxhistoryid)` |  |

### Table `transaction.inboxtransaction` <a id="table-transaction-inboxtransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `inboxtransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `inboxid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inboxid)` |  |

### Table `transaction.individualdonor` <a id="table-transaction-individualdonor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `individualdonor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `gender` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `birthplace` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `birthdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `identitytype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `identitynumber` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `language` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `lastformaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `incomepermonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `expensepermonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `maritalstate` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `officeaddress` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `officekelurahan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `officesubdistrict` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `officecity` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `officestate` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `officepostalcode` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `officephonenumber` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `email` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 20 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 21 | `mobilephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 22 | `idpropinsioffice` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `officekecamatan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `corporatename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `jobposition` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `couplename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `fworkid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `child` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `isinternalemployee` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `workareaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `workunitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `workidentitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `statusrumah` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `transaction.intrnewtransaction` <a id="table-transaction-intrnewtransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `intrnewtransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsysteminteraction_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `dialogid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `processingscriptid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `numbertag` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `servermethodid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsysteminteraction_id)` |  |

### Table `transaction.intrpicktransaction` <a id="table-transaction-intrpicktransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `intrpicktransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsysteminteraction_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `dialogid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `numbertag` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsysteminteraction_id)` |  |

### Table `transaction.inventory` <a id="table-transaction-inventory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `inventory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `nilaiawal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilaisisa` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `qtysisa` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `qtytotal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `inventorycategoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.inventorycategory` <a id="table-transaction-inventorycategory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `inventorycategory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `inventorycategoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentinventorycategoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `inventorycategorycode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inventorycategoryname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inventorycategoryid)` |  |

### Table `transaction.investee` <a id="table-transaction-investee"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `investee` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `investeeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `investeename` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `investeecode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `investeephone` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `investeeaddress` | `character varying(250)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `investeenisbah` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (investeeid)` |  |

### Table `transaction.investment` <a id="table-transaction-investment"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `investment` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `managerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `investmentamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `investmentcatid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `investmentshare` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `lifetime` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `investmenttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `investeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `startdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `investmentnisbah` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `investmentdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.investmentcategory` <a id="table-transaction-investmentcategory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `investmentcategory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `investmentcatid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `investmentcatname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `investmentcatcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `investmentcattype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (investmentcatid)` |  |

### Table `transaction.investmentmanager` <a id="table-transaction-investmentmanager"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `investmentmanager` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `managerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `managercode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `managername` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (managerid)` |  |

### Table `transaction.invoice` <a id="table-transaction-invoice"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `invoice` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invoiceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `invoicedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `invoiceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `invoicetype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `invoiceamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `invoicepaymentstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `paymenttransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invoiceid)` |  |

### Table `transaction.invoicefa` <a id="table-transaction-invoicefa"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `invoicefa` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invoiceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invoiceid)` |  |

### Table `transaction.invoiceproduct` <a id="table-transaction-invoiceproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `invoiceproduct` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invoiceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `invoiceaddress` | `character varying(250)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `invoicebankname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `invoicebankaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `invoicebankaccountnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `invoiceofficername` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `invoiceofficerposition` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `invoicetermdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `productaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `invoicecontactperson` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `invoicecontactphone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invoiceid)` |  |

### Table `transaction.invoiceproductdefaultdata` <a id="table-transaction-invoiceproductdefaultdata"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `invoiceproductdefaultdata` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branchcode` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `invoicebankname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `invoicebankaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `invoicebankaccountnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `invoiceofficername` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `invoiceofficerposition` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `invoicecontactperson` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `invoicecontactphone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branchcode)` |  |

### Table `transaction.jenis_dana` <a id="table-transaction-jenis-dana"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `jenis_dana` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_jenis_dana` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_jenis_dana` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_jenis_dana)` |  |

### Table `transaction.jenisrak` <a id="table-transaction-jenisrak"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `jenisrak` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `koderak` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountcode_rakpusat` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jenisrak` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (koderak)` |  |

### Table `transaction.journal` <a id="table-transaction-journal"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journal` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `source_app` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no)` |  |

### Table `transaction.journal_bck` <a id="table-transaction-journal-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journal_bck` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `source_app` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.journal_bck20150821` <a id="table-transaction-journal-bck20150821"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journal_bck20150821` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `source_app` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.journal_cashflow` <a id="table-transaction-journal-cashflow"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journal_cashflow` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cfgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no)` |  |

### Table `transaction.journal_cashflow_candidate` <a id="table-transaction-journal-cashflow-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journal_cashflow_candidate` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no)` |  |

### Table `transaction.journalblock` <a id="table-transaction-journalblock"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journalblock` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `system_id` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `class_id` | `character varying(32)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `key_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id_journalblock` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `dataid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `journal_no` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `subsystemcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transaction_tag` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_journalblock)` |  |

### Table `transaction.journalcode` <a id="table-transaction-journalcode"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journalcode` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_ubah` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `terminal_ubah` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tanggal_ubah` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `journalcode_id` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journalcode_id)` |  |

### Table `transaction.journaldeletion` <a id="table-transaction-journaldeletion"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journaldeletion` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `user_terminal` | `character varying(23)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `process_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no)` |  |

### Table `transaction.journalitem` <a id="table-transaction-journalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journalitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `journalitem_no` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `amount_debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount_credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `nilai_kurs` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fl_journal, journalitem_no)` |  |

### Table `transaction.journalitem_cashflow` <a id="table-transaction-journalitem-cashflow"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `journalitem_cashflow` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `journalitem_no` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `cfgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no, journalitem_no)` |  |

### Table `transaction.kota_kabupaten` <a id="table-transaction-kota-kabupaten"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `kota_kabupaten` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kotaid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kota_kabupaten` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kotaid)` |  |

### Table `transaction.kurshistory` <a id="table-transaction-kurshistory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `kurshistory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kurshistory_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kurs_beli_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `kurs_jual_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `history_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `user_ubah` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `terminal_pengubah` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kurshistory_id)` |  |

### Table `transaction.mapaccount` <a id="table-transaction-mapaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mapaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `oldaccount` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `newaccount` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.mapping_gldetail_2014` <a id="table-transaction-mapping-gldetail-2014"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mapping_gldetail_2014` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code_old` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code_new` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code_old)` |  |

### Table `transaction.mapping_glint_asset` <a id="table-transaction-mapping-glint-asset"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mapping_glint_asset` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code_new` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code)` |  |

### Table `transaction.mapping_glinttemplate_2014` <a id="table-transaction-mapping-glinttemplate-2014"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mapping_glinttemplate_2014` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productcode` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `template_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productcode)` |  |

### Table `transaction.mappingcoa` <a id="table-transaction-mappingcoa"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mappingcoa` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code_lama` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code_baru` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code_lama)` |  |

### Table `transaction.mapreconcile` <a id="table-transaction-mapreconcile"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mapreconcile` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mapid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mapdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mapproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mapfundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mapprocesstype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isapplytoallaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `bankaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `mapaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `mapmutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mapaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mapid)` |  |

### Table `transaction.mapreconcileaccount` <a id="table-transaction-mapreconcileaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mapreconcileaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mapaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mapid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankcashaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mapaccountid)` |  |

### Table `transaction.masterkurs` <a id="table-transaction-masterkurs"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `masterkurs` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_kurs` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_kurs` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nama_field_currency` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `rpv_name` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_kurs)` |  |

### Table `transaction.mustahiq` <a id="table-transaction-mustahiq"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mustahiq` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqaddress` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `mustahiqname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mustahiqreferenceby` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqstatus` | `character(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `mustahiqno` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mustahiqaddresskelurahan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `mustahiqaddresskecamatan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `mustahiqpostalcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.mustahiqbankaccount` <a id="table-transaction-mustahiqbankaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mustahiqbankaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `transaction.mustahiqcorporate` <a id="table-transaction-mustahiqcorporate"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mustahiqcorporate` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cpmobilenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cpphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.mustahiqpersonal` <a id="table-transaction-mustahiqpersonal"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `mustahiqpersonal` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqbirthdate` | `date` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `mustahiqbirthplace` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mustahiqformaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqgender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqidentitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `mustahiqmarital` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqreligion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `mustahiqtotalfamily` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `mustahiqincome` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `mustahiqidentitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `mustahiqworksector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.negara` <a id="table-transaction-negara"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `negara` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idnegara` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_negara` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idnegara)` |  |

### Table `transaction.parameter` <a id="table-transaction-parameter"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `parameter` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parametercode` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parametervalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parameterstringvalue` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `parameterdatevalue` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parametercode)` |  |

### Table `transaction.parameterglobal` <a id="table-transaction-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `parameterglobal` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(25)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_parameter)` |  |

### Table `transaction.parameterglobaltes` <a id="table-transaction-parameterglobaltes"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `parameterglobaltes` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.parameterinbox` <a id="table-transaction-parameterinbox"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `parameterinbox` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kodeinbox` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `namaform` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `taginbox` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kodeinbox)` |  |

### Table `transaction.parameterjournal` <a id="table-transaction-parameterjournal"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `parameterjournal` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterjournalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `journalcode` | `character varying(5)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `datasource` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterjournalid)` |  |

### Table `transaction.parameterjournalitem` <a id="table-transaction-parameterjournalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `parameterjournalitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterjournalitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchbase` | `character varying(1)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `basesign` | `character varying(1)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currencybase` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `amountbase` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `ratebase` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `parameterjournalid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `accountbase` | `character varying(1)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `issendjournaldescription` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `issendrccode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterjournalitemid)` |  |

### Table `transaction.periodebalance` <a id="table-transaction-periodebalance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `periodebalance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodebalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periodebalance_id)` |  |

### Table `transaction.periodeprojectbalance` <a id="table-transaction-periodeprojectbalance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `periodeprojectbalance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodeprojectbalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periodeprojectbalance_id)` |  |

### Table `transaction.product` <a id="table-transaction-product"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `product` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productname` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountofcollection` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountofdistribution` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `percentageofamilfunds` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `producttype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `closeddate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `fundcategory` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fixedvalue` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `fixedvalueamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `multipackage` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `nishab` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `haul` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `parentproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `isdetail` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `productcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `zakahobjectid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `zakahobject` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `programtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `programcategory` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `transaction.productaccount` <a id="table-transaction-productaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `productaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `zakatbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `infaqbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `infaqterikatbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `wakafbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `amilbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `nonhalalbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `producttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `transaction.producthierarchy` <a id="table-transaction-producthierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `producthierarchy` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `hierarchyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `childproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (hierarchyid)` |  |

### Table `transaction.project` <a id="table-transaction-project"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `project` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `project_no` | `character varying(10)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `name` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(255)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `manager` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `start_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `end_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.projectsponsordisbursement` <a id="table-transaction-projectsponsordisbursement"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `projectsponsordisbursement` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `disbid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `disbnumber` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `disbdateplan` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `disbamountplan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isdisbursed` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `projectsponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (disbid)` |  |

### Table `transaction.propinsi` <a id="table-transaction-propinsi"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `propinsi` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idpropinsi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `propinsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kodepropinsi` | `character varying(3)` | YES | NULL::character varying | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idpropinsi)` |  |
| `kode_unik` | UNIQUE | `UNIQUE (kodepropinsi)` |  |

### Table `transaction.prospectivedonor` <a id="table-transaction-prospectivedonor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `prospectivedonor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `prospectivedonorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `phonenumber` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `donorname` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `referenceby` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (prospectivedonorid)` |  |

### Table `transaction.rakcabang` <a id="table-transaction-rakcabang"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `rakcabang` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rakcabang_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `koderak` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rakcabang_id)` |  |

### Table `transaction.rakpusat` <a id="table-transaction-rakpusat"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `rakpusat` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rakpusat_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `koderak` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rakpusat_id)` |  |

### Table `transaction.reconcileaccountbalance` <a id="table-transaction-reconcileaccountbalance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `reconcileaccountbalance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountbalanceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `beginbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `reconciledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountbalanceid)` |  |

### Table `transaction.reconciletransaction` <a id="table-transaction-reconciletransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `reconciletransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `banktransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `accountdebet` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `reconstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `processstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `referenceno` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `processaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `processaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (banktransactionid)` |  |

### Table `transaction.reconciletransactionbck` <a id="table-transaction-reconciletransactionbck"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `reconciletransactionbck` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `banktransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountcredit` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountdebet` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `reconstatus` | `boolean` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `processstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.registerkurs` <a id="table-transaction-registerkurs"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `registerkurs` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `registerkurs_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_ubah` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `terminal_ubah` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `tanggal_ubah` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kurs_beli_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kurs_jual_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kode_register` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (registerkurs_id)` |  |

### Table `transaction.rekeningbmm` <a id="table-transaction-rekeningbmm"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `rekeningbmm` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomorrekening` | `character varying(20)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (nomorrekening)` |  |

### Table `transaction.revaluationhistory` <a id="table-transaction-revaluationhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `revaluationhistory` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `history_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `revaluation_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `average_exchangerate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `revaluation_exchangerate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (history_id)` |  |

### Table `transaction.reversetransaction` <a id="table-transaction-reversetransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `reversetransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `sourcetransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `revtransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (sourcetransactionid)` |  |

### Table `transaction.rpvaccount` <a id="table-transaction-rpvaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `rpvaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rpv_name` | `character varying(20)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `rpv_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `profit_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `loss_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rpv_name)` |  |

### Table `transaction.rpvaccountdetail` <a id="table-transaction-rpvaccountdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `rpvaccountdetail` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_valas` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountinstance_primer` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `rpvaccountdetail_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `currency_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `rpv_name` | `character varying(20)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 6 | `branch_code` | `character varying(5)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code, rpv_name, branch_code)` |  |

### Table `transaction.salestransaction` <a id="table-transaction-salestransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `salestransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salespersonname` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `transaction.script_collection` <a id="table-transaction-script-collection"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `script_collection` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `script_code` | `character varying(15)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `script_name` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `script_description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `script_path` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (script_code)` |  |

### Table `transaction.sessionblob` <a id="table-transaction-sessionblob"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `sessionblob` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sessionid` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sessioncontext` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `transaction.sim_logrun` <a id="table-transaction-sim-logrun"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `sim_logrun` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `logrun_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sim_userid` | `character varying` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sim_type` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `completion_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `status` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(255)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (logrun_id)` |  |

### Table `transaction.snapshot_accountinstance` <a id="table-transaction-snapshot-accountinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `snapshot_accountinstance` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_cpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fl_lpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isbolehinput` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `currency_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periodebalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.sponsor` <a id="table-transaction-sponsor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `sponsor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `sponsorid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `name` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `address` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `contactpersonname` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `contactpersonnumber` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (sponsorid)` |  |

### Table `transaction.sponsortransaction` <a id="table-transaction-sponsortransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `sponsortransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `projectsponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `sttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `invoicestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `invoicedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `invoiceno` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.subsysteminteraction` <a id="table-transaction-subsysteminteraction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `subsysteminteraction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsysteminteraction_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `titleinteraction` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentssi_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `interactiontype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `intrmodel` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `subsystemcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsysteminteraction_id)` |  |

### Table `transaction.tempcandidatejournal` <a id="table-transaction-tempcandidatejournal"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tempcandidatejournal` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `tempcandidatejournal_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branch_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `group_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kode_kurs` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kode_mutasi` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `nilai_kurs` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `nilai_mutasi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (tempcandidatejournal_id)` |  |

### Table `transaction.temptable` <a id="table-transaction-temptable"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `temptable` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.temptable_ori` <a id="table-transaction-temptable-ori"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `temptable_ori` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountcode)` |  |

### Table `transaction.temptabledata` <a id="table-transaction-temptabledata"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `temptabledata` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.temptablenew` <a id="table-transaction-temptablenew"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `temptablenew` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountcode)` |  |

### Table `transaction.tmp_accounttransactionitem_bck` <a id="table-transaction-tmp-accounttransactionitem-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_accounttransactionitem_bck` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounttitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `amountperunit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `totalunit` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `percentageofamil` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `distributionitemaccount` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `cattype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `returntransactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `catransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `isupdatebalance` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `distributiontransferid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kota` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `kecamatan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `distributioncategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `fundaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

### Table `transaction.tmp_acctranitem_repair_zakat2` <a id="table-transaction-tmp-acctranitem-repair-zakat2"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_acctranitem_repair_zakat2` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounttitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `amountperunit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `totalunit` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `percentageofamil` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `distributionitemaccount` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `cattype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `returntransactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `catransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `isupdatebalance` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `distributiontransferid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kota` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `kecamatan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `distributioncategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `fundaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

### Table `transaction.tmp_deletedaccount` <a id="table-transaction-tmp-deletedaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_deletedaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code)` |  |

### Table `transaction.tmp_gen_productaccount` <a id="table-transaction-tmp-gen-productaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_gen_productaccount` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productname` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `currencycode` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid, branchcode, currencycode)` |  |

### Table `transaction.tmp_hctransactiongroup` <a id="table-transaction-tmp-hctransactiongroup"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_hctransactiongroup` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `fundentity` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `channelaccountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 7 | `productaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `amount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid, fundentity, channelaccountno)` |  |

### Table `transaction.tmp_journalitem_bck` <a id="table-transaction-tmp-journalitem-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_journalitem_bck` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `amount_debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount_credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `nilai_kurs` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_mapping_repair_zakat` <a id="table-transaction-tmp-mapping-repair-zakat"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_mapping_repair_zakat` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno_old` | `character varying(20)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `accountno_new` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `accountcode_old` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountcode_new` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountname_old` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `accountname_new` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `productid_old` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `productid_new` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `productname_old` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `productname_new` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno_old)` |  |

### Table `transaction.tmp_mappingproduct1` <a id="table-transaction-tmp-mappingproduct1"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_mappingproduct1` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `oldproductcode` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `oldaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `oldaccountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `programtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `programcategory` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `programproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fundentity` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 8 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactionproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `newproductcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `newproductname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `newaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `newtranproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `newprogproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (oldproductcode, fundentity)` |  |

### Table `transaction.tmp_mappingtran_accountcode` <a id="table-transaction-tmp-mappingtran-accountcode"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_mappingtran_accountcode` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.tmp_mappingtran_accountcode2` <a id="table-transaction-tmp-mappingtran-accountcode2"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_mappingtran_accountcode2` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.tmp_newprogramname` <a id="table-transaction-tmp-newprogramname"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_newprogramname` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `productname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `newproductname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_program` <a id="table-transaction-tmp-program"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_program` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `tranproductcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `productname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tranproductname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balance` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_repair_journalamil` <a id="table-transaction-tmp-repair-journalamil"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_repair_journalamil` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_repair_phpinfaq` <a id="table-transaction-tmp-repair-phpinfaq"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_repair_phpinfaq` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `actualdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fundaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_repair_porsiamilinfaq` <a id="table-transaction-tmp-repair-porsiamilinfaq"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_repair_porsiamilinfaq` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `fundaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_tranitem_repair_zakat2` <a id="table-transaction-tmp-tranitem-repair-zakat2"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_tranitem_repair_zakat2` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_tranitem_repair_zakat_bck1` <a id="table-transaction-tmp-tranitem-repair-zakat-bck1"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_tranitem_repair_zakat_bck1` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.tmp_transactiongroup` <a id="table-transaction-tmp-transactiongroup"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_transactiongroup` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `productaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `amount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Indexes

| Nama | Kolom | Unique | Method | Predicate | Catatan |
| --- | --- | --- | --- | --- | --- |
| `idx_tmp_transactiongroup1` | `donorid`, `fundentity`, `channelaccountno` | NO | btree |  | needs_review |

### Table `transaction.tmp_transactionitem_bck` <a id="table-transaction-tmp-transactionitem-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `tmp_transactionitem_bck` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transaction` <a id="table-transaction-transaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputer` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `authuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactiontime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `authstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `isposted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `journalblockid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `channelcode` | `character varying` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `volunteerid` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `actualdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `paidto` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 24 | `donorname` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 25 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `receivedfrom` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 30 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `hcbatchitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `authoperationmode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `updatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `journalerrordescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `flag_omit_journal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transactionbatch` <a id="table-transaction-transactionbatch"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transactionbatch` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `batchid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `batchno` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `batchdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `branchcode` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `inputer` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `isclosed` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isposted` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `batchtag` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (batchid)` |  |

### Table `transaction.transactionitem` <a id="table-transaction-transactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transactionitem` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `transaction.transactionitem_inject` <a id="table-transaction-transactionitem-inject"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transactionitem_inject` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transactiontype` <a id="table-transaction-transactiontype"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transactiontype` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactioncode` | `character varying(10)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `vouchercode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transaksirak` <a id="table-transaction-transaksirak"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transaksirak` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cabangasal` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cabangtujuan` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `jenistransaksirak` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transaksirak_id` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `keterangan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `statusterprosespusat` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transaksirakterkait_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `journal_no` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `koderak` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transhistoryofchanges` <a id="table-transaction-transhistoryofchanges"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transhistoryofchanges` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `historyid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `newtransactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `processtime` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `changetype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transitemglinterface` <a id="table-transaction-transitemglinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transitemglinterface` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glinterfacecode` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionitemid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.transrecongenlog` <a id="table-transaction-transrecongenlog"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `transrecongenlog` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `logid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `banktransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.userapp_` <a id="table-transaction-userapp-"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `userapp_` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `user_id` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `username` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nolimitlocation` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `login_count` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mod_user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `user_id1` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.userapp_old` <a id="table-transaction-userapp-old"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `userapp_old` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `user_id` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `username` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nolimitlocation` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `login_count` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mod_user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `user_id1` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.usergroup` <a id="table-transaction-usergroup"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `usergroup` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `group_id` | `character varying(8)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `groupname` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.usergroup_` <a id="table-transaction-usergroup-"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `usergroup_` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `group_id` | `character varying(8)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `groupname` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.usergroupapp` <a id="table-transaction-usergroupapp"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `usergroupapp` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `user_id` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `group_id` | `character varying(8)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.usergroupapp_` <a id="table-transaction-usergroupapp-"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `usergroupapp_` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `user_id` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `group_id` | `character varying(8)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.vendor` <a id="table-transaction-vendor"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `vendor` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `name` | `character varying(40)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `address` | `character varying(60)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `post_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `tlp_no` | `character varying(14)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `vendor_no` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.volunteer` <a id="table-transaction-volunteer"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `volunteer` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `volunteerid` | `character varying(10)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `volunteername` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `totalamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `homeaddress` | `character varying(150)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `homephone` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `mobilephone` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `email` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

### Table `transaction.volunteertransaction` <a id="table-transaction-volunteertransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `volunteertransaction` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `volunteerid` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.wakafcertificate` <a id="table-transaction-wakafcertificate"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `wakafcertificate` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `certificateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `certificatenumber` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `certificatedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `certificatedescription` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (certificateid)` |  |

### Table `transaction.workarea` <a id="table-transaction-workarea"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `workarea` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workareaid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `workareacode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workareaname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `transaction.workunit` <a id="table-transaction-workunit"></a>

| Field | Value |
| --- | --- |
| Schema | `transaction` |
| Table | `workunit` |
| Domain | `Needs Review` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `workunitcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workunitname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
