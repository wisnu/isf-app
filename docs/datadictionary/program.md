# Data Dictionary — Schema `program`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `program`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_activityappraisal` | `program` |  | needs_review | 24 | 24 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_activityappraisalitem` | `program` |  | needs_review | 56 | 56 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_activityappraisalitemtemplate` | `program` |  | needs_review | 45 | 45 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_agenda` | `program` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_agendaitem` | `program` |  | needs_review | 6 | 6 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_agendaitemtemplate` | `program` |  | needs_review | 14 | 14 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_agendatemplate` | `program` |  | needs_review | 4 | 4 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_appraisal` | `program` |  | needs_review | 36 | 36 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_appraisalitem` | `program` |  | needs_review | 377 | 377 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_appraisalitemtemplate` | `program` |  | needs_review | 100 | 100 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_aqhpropose` | `program` |  | needs_review | 26 | 26 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bankaccountlist` | `program` |  | needs_review | 103 | 103 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_companion` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_companionvisit` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_companionvisititem` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_companionvisititemtemplate` | `program` |  | needs_review | 10 | 10 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_costitem` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_customer` | `program` |  | needs_review | 379 | 379 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_detailklaimtransaksiproject` | `program` |  | needs_review | 5 | 5 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donor` | `program` |  | needs_review | 65 | 65 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_event` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_eventplan` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_itemuploadedstatement` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_klaimtransaksiproject` | `program` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_linkedprograms` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_marketingqurban` | `program` |  | needs_review | 27 | 27 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_masterjenisdonasiqurban` | `program` |  | needs_review | 6 | 6 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mpzzisallocation` | `program` |  | needs_review | 5 | 5 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiq` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiqadditionalinfo` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiqgroup` | `program` |  | needs_review | 246 | 246 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiqproduct` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiqproductgroup` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_orphandebtlist` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_orphansiblings` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_orphantertiarylist` | `program` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_partner` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_picdistribusi` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_product` | `program` |  | needs_review | 40 | 40 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_productdetail` | `program` |  | needs_review | 10 | 10 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_productgroup` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_proposal` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realization` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationbudget` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationcost` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationdetail` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationmemo` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationmemodetail` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationpartner` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationphoto` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationreturn` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_realizationreturndetail` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_reconcileprocess` | `program` |  | needs_review | 43 | 43 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_region` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_rekeningpenghimpunanqurban` | `program` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_requestdistribusi` | `program` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_statusreceivablereport` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_statusrecrepdetail` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transaction` | `program` |  | needs_review | 19 | 19 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionitem` | `program` |  | needs_review | 26 | 26 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_uploadedstatement` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_visit` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_visititem` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_visitperson` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_worksector` | `program` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Views

| Nama | Schema | Catatan |
| --- | --- | --- |
| `dcamountpartition` | `program` | needs_review (definisi view lihat DDL sumber) |
| `mnrtransaction` | `program` | needs_review (definisi view lihat DDL sumber) |
| `v_mustahiq` | `program` | needs_review (definisi view lihat DDL sumber) |
| `v_mustahiqdata` | `program` | needs_review (definisi view lihat DDL sumber) |
| `v_reconcilequrban` | `program` | needs_review (definisi view lihat DDL sumber) |
| `v_reconciletransaction` | `program` | needs_review (definisi view lihat DDL sumber) |
| `vemployee` | `program` | needs_review (definisi view lihat DDL sumber) |

## Tables

Daftar table:

- [`program.account`](#table-program-account) — 4 kolom
- [`program.accounttransactionitem`](#table-program-accounttransactionitem) — 5 kolom
- [`program.activityappraisal`](#table-program-activityappraisal) — 11 kolom
- [`program.activityappraisalitem`](#table-program-activityappraisalitem) — 7 kolom
- [`program.activityappraisalitemtemplate`](#table-program-activityappraisalitemtemplate) — 14 kolom
- [`program.agenda`](#table-program-agenda) — 5 kolom
- [`program.agendaitem`](#table-program-agendaitem) — 4 kolom
- [`program.agendaitemtemplate`](#table-program-agendaitemtemplate) — 5 kolom
- [`program.agendatemplate`](#table-program-agendatemplate) — 5 kolom
- [`program.appraisal`](#table-program-appraisal) — 13 kolom
- [`program.appraisalitem`](#table-program-appraisalitem) — 7 kolom
- [`program.appraisalitemgroup`](#table-program-appraisalitemgroup) — 2 kolom
- [`program.appraisalitemtemplate`](#table-program-appraisalitemtemplate) — 14 kolom
- [`program.appraisaltemplate`](#table-program-appraisaltemplate) — 4 kolom
- [`program.aqhpropose`](#table-program-aqhpropose) — 11 kolom
- [`program.assetcategory`](#table-program-assetcategory) — 12 kolom
- [`program.balancepartition`](#table-program-balancepartition) — 5 kolom
- [`program.bank`](#table-program-bank) — 3 kolom
- [`program.bankaccountlist`](#table-program-bankaccountlist) — 6 kolom
- [`program.blobregistration`](#table-program-blobregistration) — 3 kolom
- [`program.branch`](#table-program-branch) — 5 kolom
- [`program.branchbankpic`](#table-program-branchbankpic) — 10 kolom
- [`program.branchlocation`](#table-program-branchlocation) — 6 kolom
- [`program.cashadvancereturninfo`](#table-program-cashadvancereturninfo) — 3 kolom
- [`program.claimitem`](#table-program-claimitem) — 5 kolom
- [`program.claimtransactiondetailqurban`](#table-program-claimtransactiondetailqurban) — 6 kolom
- [`program.claimtransactionqurban`](#table-program-claimtransactionqurban) — 2 kolom
- [`program.companion`](#table-program-companion) — 4 kolom
- [`program.companioncontract`](#table-program-companioncontract) — 14 kolom
- [`program.companionliabilityaccount`](#table-program-companionliabilityaccount) — 3 kolom
- [`program.companionpersonalkum3`](#table-program-companionpersonalkum3) — 4 kolom
- [`program.companionproduct`](#table-program-companionproduct) — 3 kolom
- [`program.companionvisit`](#table-program-companionvisit) — 9 kolom
- [`program.companionvisititem`](#table-program-companionvisititem) — 7 kolom
- [`program.companionvisititemtemplate`](#table-program-companionvisititemtemplate) — 12 kolom
- [`program.corporatedonor`](#table-program-corporatedonor) — 14 kolom
- [`program.costitem`](#table-program-costitem) — 3 kolom
- [`program.currency`](#table-program-currency) — 4 kolom
- [`program.custom_idgen`](#table-program-custom-idgen) — 4 kolom
- [`program.customer`](#table-program-customer) — 18 kolom
- [`program.customercorporate`](#table-program-customercorporate) — 7 kolom
- [`program.customerorphan`](#table-program-customerorphan) — 36 kolom
- [`program.customerpersonal`](#table-program-customerpersonal) — 13 kolom
- [`program.daerahdistribusi`](#table-program-daerahdistribusi) — 7 kolom
- [`program.detailklaimtransaksiproject`](#table-program-detailklaimtransaksiproject) — 3 kolom
- [`program.disease`](#table-program-disease) — 2 kolom
- [`program.diseasediagnosed`](#table-program-diseasediagnosed) — 4 kolom
- [`program.donor`](#table-program-donor) — 23 kolom
- [`program.donorbankaccount`](#table-program-donorbankaccount) — 2 kolom
- [`program.donorliabilityaccount`](#table-program-donorliabilityaccount) — 3 kolom
- [`program.donormember`](#table-program-donormember) — 2 kolom
- [`program.donorpersonal`](#table-program-donorpersonal) — 1 kolom
- [`program.donorproduct`](#table-program-donorproduct) — 3 kolom
- [`program.employee`](#table-program-employee) — 8 kolom
- [`program.enum_int`](#table-program-enum-int) — 3 kolom
- [`program.enum_varchar`](#table-program-enum-varchar) — 3 kolom
- [`program.event`](#table-program-event) — 7 kolom
- [`program.eventattendance`](#table-program-eventattendance) — 4 kolom
- [`program.eventksm`](#table-program-eventksm) — 3 kolom
- [`program.eventplan`](#table-program-eventplan) — 11 kolom
- [`program.eventplanattendance`](#table-program-eventplanattendance) — 3 kolom
- [`program.eventplanksm`](#table-program-eventplanksm) — 8 kolom
- [`program.externaldebtor`](#table-program-externaldebtor) — 7 kolom
- [`program.financialaccount`](#table-program-financialaccount) — 11 kolom
- [`program.financingaccount`](#table-program-financingaccount) — 17 kolom
- [`program.financingtransactionitem`](#table-program-financingtransactionitem) — 2 kolom
- [`program.glinterface`](#table-program-glinterface) — 6 kolom
- [`program.glinterfacecontainer`](#table-program-glinterfacecontainer) — 3 kolom
- [`program.glinterfacemember`](#table-program-glinterfacemember) — 6 kolom
- [`program.healthliabilitytransactionitem`](#table-program-healthliabilitytransactionitem) — 6 kolom
- [`program.historyofchanges`](#table-program-historyofchanges) — 10 kolom
- [`program.id_gen`](#table-program-id-gen) — 3 kolom
- [`program.inbox`](#table-program-inbox) — 10 kolom
- [`program.inboxhistory`](#table-program-inboxhistory) — 7 kolom
- [`program.inboxtransaction`](#table-program-inboxtransaction) — 2 kolom
- [`program.individualdonor`](#table-program-individualdonor) — 28 kolom
- [`program.itemuploadedstatement`](#table-program-itemuploadedstatement) — 13 kolom
- [`program.kjks`](#table-program-kjks) — 18 kolom
- [`program.klaimtransaksiproject`](#table-program-klaimtransaksiproject) — 10 kolom
- [`program.konversiperolehanqurban`](#table-program-konversiperolehanqurban) — 6 kolom
- [`program.liabilityaccount`](#table-program-liabilityaccount) — 2 kolom
- [`program.liabilitytransactionitem`](#table-program-liabilitytransactionitem) — 3 kolom
- [`program.linkedprograms`](#table-program-linkedprograms) — 3 kolom
- [`program.mapreconcile`](#table-program-mapreconcile) — 4 kolom
- [`program.marginitem`](#table-program-marginitem) — 7 kolom
- [`program.marketingqurban`](#table-program-marketingqurban) — 6 kolom
- [`program.masjidkum3`](#table-program-masjidkum3) — 22 kolom
- [`program.masterjenisdonasiqurban`](#table-program-masterjenisdonasiqurban) — 6 kolom
- [`program.mpz`](#table-program-mpz) — 8 kolom
- [`program.mpzzisallocation`](#table-program-mpzzisallocation) — 5 kolom
- [`program.mustahiq`](#table-program-mustahiq) — 7 kolom
- [`program.mustahiqadditionalinfo`](#table-program-mustahiqadditionalinfo) — 19 kolom
- [`program.mustahiqappraisal`](#table-program-mustahiqappraisal) — 3 kolom
- [`program.mustahiqaqh`](#table-program-mustahiqaqh) — 7 kolom
- [`program.mustahiqbankaccount`](#table-program-mustahiqbankaccount) — 10 kolom
- [`program.mustahiqcandidate`](#table-program-mustahiqcandidate) — 14 kolom
- [`program.mustahiqcorporate`](#table-program-mustahiqcorporate) — 4 kolom
- [`program.mustahiqgroup`](#table-program-mustahiqgroup) — 9 kolom
- [`program.mustahiqgroupdetail`](#table-program-mustahiqgroupdetail) — 5 kolom
- [`program.mustahiqkum3`](#table-program-mustahiqkum3) — 5 kolom
- [`program.mustahiqliabilityaccount`](#table-program-mustahiqliabilityaccount) — 5 kolom
- [`program.mustahiqpersonal`](#table-program-mustahiqpersonal) — 17 kolom
- [`program.mustahiqproduct`](#table-program-mustahiqproduct) — 26 kolom
- [`program.mustahiqproductgroup`](#table-program-mustahiqproductgroup) — 4 kolom
- [`program.mustahiqproject`](#table-program-mustahiqproject) — 4 kolom
- [`program.mustahiqqurban`](#table-program-mustahiqqurban) — 4 kolom
- [`program.negara`](#table-program-negara) — 2 kolom
- [`program.orphanbalancepartition`](#table-program-orphanbalancepartition) — 2 kolom
- [`program.orphanbeasiswa`](#table-program-orphanbeasiswa) — 33 kolom
- [`program.orphandebtlist`](#table-program-orphandebtlist) — 4 kolom
- [`program.orphankafala`](#table-program-orphankafala) — 22 kolom
- [`program.orphankafalaliability`](#table-program-orphankafalaliability) — 1 kolom
- [`program.orphanksm`](#table-program-orphanksm) — 4 kolom
- [`program.orphansiblings`](#table-program-orphansiblings) — 3 kolom
- [`program.orphantertiarylist`](#table-program-orphantertiarylist) — 4 kolom
- [`program.parameterglobal`](#table-program-parameterglobal) — 9 kolom
- [`program.parameterinbox`](#table-program-parameterinbox) — 4 kolom
- [`program.parameterjournal`](#table-program-parameterjournal) — 4 kolom
- [`program.parameterjournalitem`](#table-program-parameterjournalitem) — 10 kolom
- [`program.partner`](#table-program-partner) — 9 kolom
- [`program.pequrban`](#table-program-pequrban) — 8 kolom
- [`program.perolehanqurban`](#table-program-perolehanqurban) — 10 kolom
- [`program.picdistribusi`](#table-program-picdistribusi) — 4 kolom
- [`program.product`](#table-program-product) — 26 kolom
- [`program.productaccount`](#table-program-productaccount) — 3 kolom
- [`program.productdetail`](#table-program-productdetail) — 5 kolom
- [`program.productgroup`](#table-program-productgroup) — 6 kolom
- [`program.producthierarchy`](#table-program-producthierarchy) — 4 kolom
- [`program.producttarget`](#table-program-producttarget) — 5 kolom
- [`program.producttargetcomponent`](#table-program-producttargetcomponent) — 6 kolom
- [`program.producttargethistory`](#table-program-producttargethistory) — 4 kolom
- [`program.producttransactionitem`](#table-program-producttransactionitem) — 3 kolom
- [`program.program`](#table-program-program) — 2 kolom
- [`program.programaqh`](#table-program-programaqh) — 4 kolom
- [`program.programksm`](#table-program-programksm) — 2 kolom
- [`program.programqurban`](#table-program-programqurban) — 4 kolom
- [`program.project`](#table-program-project) — 4 kolom
- [`program.projectaccount`](#table-program-projectaccount) — 4 kolom
- [`program.propinsi`](#table-program-propinsi) — 4 kolom
- [`program.proposal`](#table-program-proposal) — 15 kolom
- [`program.realisasidistribusi`](#table-program-realisasidistribusi) — 8 kolom
- [`program.realisasidistribusihewan`](#table-program-realisasidistribusihewan) — 5 kolom
- [`program.realization`](#table-program-realization) — 17 kolom
- [`program.realizationbudget`](#table-program-realizationbudget) — 4 kolom
- [`program.realizationcost`](#table-program-realizationcost) — 7 kolom
- [`program.realizationdetail`](#table-program-realizationdetail) — 13 kolom
- [`program.realizationmemo`](#table-program-realizationmemo) — 12 kolom
- [`program.realizationmemodetail`](#table-program-realizationmemodetail) — 5 kolom
- [`program.realizationpartner`](#table-program-realizationpartner) — 3 kolom
- [`program.realizationphoto`](#table-program-realizationphoto) — 4 kolom
- [`program.realizationreturn`](#table-program-realizationreturn) — 12 kolom
- [`program.realizationreturndetail`](#table-program-realizationreturndetail) — 9 kolom
- [`program.realizationtransactionitem`](#table-program-realizationtransactionitem) — 10 kolom
- [`program.reconcileprocess`](#table-program-reconcileprocess) — 11 kolom
- [`program.reconciletransaction`](#table-program-reconciletransaction) — 6 kolom
- [`program.reconciletransactionqurban`](#table-program-reconciletransactionqurban) — 5 kolom
- [`program.region`](#table-program-region) — 3 kolom
- [`program.rekeningpenghimpunanqurban`](#table-program-rekeningpenghimpunanqurban) — 4 kolom
- [`program.rencanadistribusi`](#table-program-rencanadistribusi) — 8 kolom
- [`program.rencanadistribusihewan`](#table-program-rencanadistribusihewan) — 5 kolom
- [`program.requestdistribusi`](#table-program-requestdistribusi) — 4 kolom
- [`program.reversetransaction`](#table-program-reversetransaction) — 2 kolom
- [`program.sessionblob`](#table-program-sessionblob) — 4 kolom
- [`program.statusreceivablereport`](#table-program-statusreceivablereport) — 14 kolom
- [`program.statusrecrepdetail`](#table-program-statusrecrepdetail) — 17 kolom
- [`program.tmp_budget`](#table-program-tmp-budget) — 3 kolom
- [`program.tmp_migmustahiqproduct`](#table-program-tmp-migmustahiqproduct) — 25 kolom
- [`program.tmp_migrasikodepos`](#table-program-tmp-migrasikodepos) — 12 kolom
- [`program.transaction`](#table-program-transaction) — 31 kolom
- [`program.transactionaccount`](#table-program-transactionaccount) — 16 kolom
- [`program.transactionitem`](#table-program-transactionitem) — 16 kolom
- [`program.transactiontype`](#table-program-transactiontype) — 3 kolom
- [`program.uploadedstatement`](#table-program-uploadedstatement) — 14 kolom
- [`program.visit`](#table-program-visit) — 9 kolom
- [`program.visititem`](#table-program-visititem) — 4 kolom
- [`program.visitperson`](#table-program-visitperson) — 5 kolom
- [`program.volunteer`](#table-program-volunteer) — 8 kolom
- [`program.volunteertransaction`](#table-program-volunteertransaction) — 2 kolom
- [`program.vproduct`](#table-program-vproduct) — 12 kolom
- [`program.worksector`](#table-program-worksector) — 4 kolom

### Table `program.account` <a id="table-program-account"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `account` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_name` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `account_level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `is_detail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code)` |  |

### Table `program.accounttransactionitem` <a id="table-program-accounttransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `accounttransactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounttitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isupdatebalance` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.activityappraisal` <a id="table-program-activityappraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `activityappraisal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `activityappraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaldate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `weekperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `anualperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `appraisalyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `approvalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `otherappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `otherappraisalflag` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (activityappraisalid)` |  |

### Table `program.activityappraisalitem` <a id="table-program-activityappraisalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `activityappraisalitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `activityappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `itemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `program.activityappraisalitemtemplate` <a id="table-program-activityappraisalitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `activityappraisalitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sequenceno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `integervaluestandard` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `floatvaluestandard` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `stringvaluestandard` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `boolvaluestandard` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `itemname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `groupname` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemtemplateid)` |  |

### Table `program.agenda` <a id="table-program-agenda"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `agenda` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendaid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendatemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendaid)` |  |

### Table `program.agendaitem` <a id="table-program-agendaitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `agendaitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendaitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `agendaitemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `attendance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendaitemid)` |  |

### Table `program.agendaitemtemplate` <a id="table-program-agendaitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `agendaitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendaitemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendatemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `datevalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isevent` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `eventplanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendaitemtemplateid)` |  |

### Table `program.agendatemplate` <a id="table-program-agendatemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `agendatemplate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendatemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendaname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `monthvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `quota` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `yearvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendatemplateid)` |  |

### Table `program.appraisal` <a id="table-program-appraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `appraisal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `annualperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaldate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `appraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `appraisaltemplateid` | `integer` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 5 | `appraisalyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `approvalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `weekperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `appraisalsubject` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `subjectkeycount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `subjectkey1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `subjectkey2` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (appraisalid)` |  |

### Table `program.appraisalitem` <a id="table-program-appraisalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `appraisalitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 6 | `itemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `program.appraisalitemgroup` <a id="table-program-appraisalitemgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `appraisalitemgroup` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `groupname` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (groupname)` |  |

### Table `program.appraisalitemtemplate` <a id="table-program-appraisalitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `appraisalitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisaltemplateid` | `integer` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 2 | `boolvaluestandard` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `floatvaluestandard` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `integervaluestandard` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `islowlevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `itemname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `itemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 10 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `sequenceno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `stringvaluestandard` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemtemplateid)` |  |

### Table `program.appraisaltemplate` <a id="table-program-appraisaltemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `appraisaltemplate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisalname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaltemplateid` | `integer` | NO |  | PK | YES | full | synthetic_only | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `formula` | `character varying(285)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (appraisaltemplateid)` |  |

### Table `program.aqhpropose` <a id="table-program-aqhpropose"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `aqhpropose` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `aqhproposeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `proposeplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `proposestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `proposedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `paybackperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `purposeofuse` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `installment` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `sidate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (aqhproposeid)` |  |

### Table `program.assetcategory` <a id="table-program-assetcategory"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `assetcategory` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `assetcategoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentassetcategoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `assetcategorycode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `assetcategoryname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `defaultlifetime` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `thresholdvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputer` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `inputtime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `isdepreciable` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `assettype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (assetcategoryid)` |  |

### Table `program.balancepartition` <a id="table-program-balancepartition"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `balancepartition` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `balancepartitionid` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balancepartitiontype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `partitionclassifier` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (balancepartitionid)` |  |

### Table `program.bank` <a id="table-program-bank"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `bank` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankcode` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankshortname` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankcode)` |  |

### Table `program.bankaccountlist` <a id="table-program-bankaccountlist"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `bankaccountlist` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `bankaccountname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdefault` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `bankaccountlisttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `bankcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `program.blobregistration` <a id="table-program-blobregistration"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `blobregistration` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `actualfilename` | `character varying(128)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `istemporary` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `program.branch` <a id="table-program-branch"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `branch` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branchcode` | `character varying(3)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `shortcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branchcode)` |  |

### Table `program.branchbankpic` <a id="table-program-branchbankpic"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `branchbankpic` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branchcode` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `picname` | `character varying(250)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `activedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mobilenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `faxnumber` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `email` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `userlogin` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `phonenumber` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `picposition` | `character varying(80)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branchcode)` |  |

### Table `program.branchlocation` <a id="table-program-branchlocation"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `branchlocation` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branch_code` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `masterbranch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branch_code)` |  |

### Table `program.cashadvancereturninfo` <a id="table-program-cashadvancereturninfo"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `cashadvancereturninfo` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `sourcetransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `returntransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (sourcetransactionid)` |  |

### Table `program.claimitem` <a id="table-program-claimitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `claimitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `claimitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `residualclaim` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `claimtotal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `claimtransactionurbanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `banktransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (claimitemid)` |  |

### Table `program.claimtransactiondetailqurban` <a id="table-program-claimtransactiondetailqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `claimtransactiondetailqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `claimtransactiondetailqurbanid` | `integer CONSTRAINT claimtransactiondetailqurba_claimtransactiondetailqurb_not_null` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `claimtransactionqurbanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nominalklaim` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (claimtransactiondetailqurbanid)` |  |

### Table `program.claimtransactionqurban` <a id="table-program-claimtransactionqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `claimtransactionqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `claimtransactionqurbanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `claimtotal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (claimtransactionqurbanid)` |  |

### Table `program.companion` <a id="table-program-companion"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companion` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `companionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `companionextnumber` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (companionid)` |  |

### Table `program.companioncontract` <a id="table-program-companioncontract"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companioncontract` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `contractno` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `initialcontractperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `endcontractperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `documentfile` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `inputterminal` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `bmisupervisi` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kabkota` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `companionexperience` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (contractno)` |  |

### Table `program.companionliabilityaccount` <a id="table-program-companionliabilityaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companionliabilityaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.companionpersonalkum3` <a id="table-program-companionpersonalkum3"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companionpersonalkum3` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `workinghour` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workplace` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `workposition` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.companionproduct` <a id="table-program-companionproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companionproduct` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `companionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `contractno` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid, companionid)` |  |

### Table `program.companionvisit` <a id="table-program-companionvisit"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companionvisit` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `companionvisitid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `visitingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `visitingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `weekperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `annotation` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `approvalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (companionvisitid)` |  |

### Table `program.companionvisititem` <a id="table-program-companionvisititem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companionvisititem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `itemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `companionvisitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `program.companionvisititemtemplate` <a id="table-program-companionvisititemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `companionvisititemtemplate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sequenceno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `itemname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `visitgroup` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `answerchoice` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parentitem` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `islowlevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemtemplateid)` |  |

### Table `program.corporatedonor` <a id="table-program-corporatedonor"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `corporatedonor` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `corporation` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `siupp` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `tdp` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locationtype` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `ownertype` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `establisheddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `establishedplace` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `contactperson` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `patronagecompany` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `cpemail` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `cpphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `cpmobilenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `program.costitem` <a id="table-program-costitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `costitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `costitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `costitemcode` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `costitemdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (costitemid)` |  |

### Table `program.currency` <a id="table-program-currency"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `currency` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `currency_code` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `short_name` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `full_name` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code)` |  |

### Table `program.custom_idgen` <a id="table-program-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `custom_idgen` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idname` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idcode` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idname, idcode)` |  |

### Table `program.customer` <a id="table-program-customer"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `customer` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `customername` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `addresscity` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `addresskecamatan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `addresskelurahan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `addresspostalcode` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `addressstate` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `addressstreet` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `addresssubdistrict` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `customerno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `customerstatus` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `phonenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `customertype` | `character varying(2)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 17 | `fax` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `email` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.customercorporate` <a id="table-program-customercorporate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `customercorporate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cpphonenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `cpmobilenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `corporationnumber` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `corporationdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `cctype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.customerorphan` <a id="table-program-customerorphan"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `customerorphan` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `academicachievements` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `arthobby` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bloodtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `currentdisease` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 6 | `dreamof` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fathereducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fatherincome` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fathername` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `fatheroccupation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `guardianaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `guardiancity` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `guardiandistrict` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `guardianeducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `guardianname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `guardianoccupation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `guardianrelationship` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `guardiansubdistrict` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `guardianvillage` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `height` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `weight` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `medicalreport` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `motheraddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 24 | `mothereducation` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 25 | `motherincome` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 26 | `mothername` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 27 | `motheroccupation` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 28 | `orphanagestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `orphansubtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `physicaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `psychologicalreport` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `schoolname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `schooltype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `scores` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `skills` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `sporthobby` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.customerpersonal` <a id="table-program-customerpersonal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `customerpersonal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `birthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `birthplace` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `identitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `identitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `formaleducation` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `gender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `marital` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `totalfamily` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `worksector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `customerpersonaltype` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `workid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.daerahdistribusi` <a id="table-program-daerahdistribusi"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `daerahdistribusi` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `picdistribusiid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `alamat` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `kontakperson` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `namalokasi` | `character varying(100)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 5 | `telepon` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isrequestbaru` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `regionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (namalokasi)` |  |

### Table `program.detailklaimtransaksiproject` <a id="table-program-detailklaimtransaksiproject"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `detailklaimtransaksiproject` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `detailklaimid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idtransaksiklaim` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nominalbantuan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (detailklaimid)` |  |

### Table `program.disease` <a id="table-program-disease"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `disease` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `diseasecode` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `diseasename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (diseasecode)` |  |

### Table `program.diseasediagnosed` <a id="table-program-diseasediagnosed"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `diseasediagnosed` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `diseasediagnosedid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `diseasecode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `ishandled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (diseasediagnosedid)` |  |

### Table `program.donor` <a id="table-program-donor"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `donor` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `donorname` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `addressstreet` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `addresskelurahan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `addresssubdistrict` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `addresscity` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `addresspostalcode` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `phonenumber` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `fax` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `referenceby` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `donortype` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `addressstate` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `npwp` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `npwz` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `joindate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `addresskecamatan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 20 | `economicsector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `donoremail` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `program.donorbankaccount` <a id="table-program-donorbankaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `donorbankaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
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

### Table `program.donorliabilityaccount` <a id="table-program-donorliabilityaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `donorliabilityaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.donormember` <a id="table-program-donormember"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `donormember` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid, customerid)` |  |

### Table `program.donorpersonal` <a id="table-program-donorpersonal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `donorpersonal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `program.donorproduct` <a id="table-program-donorproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `donorproduct` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `programtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid, productid)` |  |

### Table `program.employee` <a id="table-program-employee"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `employee` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `homeaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `identitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `identityid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `birthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `birthplace` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `phonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `program.enum_int` <a id="table-program-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `enum_int` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `program.enum_varchar` <a id="table-program-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `enum_varchar` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `character varying(2)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `program.event` <a id="table-program-event"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `event` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `eventid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `eventdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `eventplanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `financingamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `reportfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `totalaudience` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `eventtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (eventid)` |  |

### Table `program.eventattendance` <a id="table-program-eventattendance"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `eventattendance` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `eventattendanceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `eventid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `eventplanattendanceid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (eventattendanceid)` |  |

### Table `program.eventksm` <a id="table-program-eventksm"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `eventksm` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `eventid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `eventdatefrom` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `eventdateto` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (eventid)` |  |

### Table `program.eventplan` <a id="table-program-eventplan"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `eventplan` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `eventplanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendaitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `eventplandescription` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `eventplanlocation` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `eventplanname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `targetaudience` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `eventplanbudget` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `eventplandate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `isreported` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `eventplantype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (eventplanid)` |  |

### Table `program.eventplanattendance` <a id="table-program-eventplanattendance"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `eventplanattendance` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `eventplanattendanceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `eventplanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (eventplanattendanceid)` |  |

### Table `program.eventplanksm` <a id="table-program-eventplanksm"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `eventplanksm` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `eventplanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `datefrom` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `dateto` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `personel` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `successindicator` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `target` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `eventtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isattendancecompleted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (eventplanid)` |  |

### Table `program.externaldebtor` <a id="table-program-externaldebtor"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `externaldebtor` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `debtorid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `debtorcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `debtorname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `debtorphone` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `debtoraddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (debtorid)` |  |

### Table `program.financialaccount` <a id="table-program-financialaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `financialaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `currencycode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `financialaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `openingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastdailybalanceid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.financingaccount` <a id="table-program-financingaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `financingaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodcount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `periodunit` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `baseamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `marginamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `basebalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `marginbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `collectibiltiylevel` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `installmentamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `installmentbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 13 | `debtarrears` | `real` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `cycleperiodcount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `realperiodcount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `graceperiodcount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.financingtransactionitem` <a id="table-program-financingtransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `financingtransactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.glinterface` <a id="table-program-glinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `glinterface` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interfaceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `interfacecode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (interfaceid)` |  |

### Table `program.glinterfacecontainer` <a id="table-program-glinterfacecontainer"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `glinterfacecontainer` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glicontainerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `glicontainercode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `glicontainername` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glicontainerid)` |  |

### Table `program.glinterfacemember` <a id="table-program-glinterfacemember"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `glinterfacemember` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glimemberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `glimembercode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glimemberid)` |  |

### Table `program.healthliabilitytransactionitem` <a id="table-program-healthliabilitytransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `healthliabilitytransactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `jenissakit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `jenisperawatan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `perkembangan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kategori` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.historyofchanges` <a id="table-program-historyofchanges"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `historyofchanges` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `historyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `changetype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `domainofchange` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `processtime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `datasourcetype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `datasourceref` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `datasourceclass` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `datasourcerefinteger` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `terminalid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (historyid)` |  |

### Table `program.id_gen` <a id="table-program-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `id_gen` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_code` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `locked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_code)` |  |

### Table `program.inbox` <a id="table-program-inbox"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `inbox` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `inboxid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `filename` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kodeinbox` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputtime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `inboxtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `lastinboxhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inboxid)` |  |

### Table `program.inboxhistory` <a id="table-program-inboxhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `inboxhistory` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `inboxhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `inboxid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `filename` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputtime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `userid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nextinboxhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inboxhistoryid)` |  |

### Table `program.inboxtransaction` <a id="table-program-inboxtransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `inboxtransaction` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `inboxid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (inboxid)` |  |

### Table `program.individualdonor` <a id="table-program-individualdonor"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `individualdonor` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `gender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `birthplace` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `birthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `identitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `identitynumber` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `maritalstate` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `language` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `lastformaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `incomepermonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `expensepermonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `officeaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `officekelurahan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `officesubdistrict` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `officecity` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `officestate` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `officepostalcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `officephonenumber` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `email` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 20 | `mobilephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 21 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 22 | `idpropinsioffice` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `officekecamatan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `jobposition` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `corporatename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `couplename` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `child` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `fworkid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `program.itemuploadedstatement` <a id="table-program-itemuploadedstatement"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `itemuploadedstatement` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `uploadedstatementid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `itemstatementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `itemrekening` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `itemdescription` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `itemdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `reconcilestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `itemamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `reconcileprocessid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `reconcileuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemstatementid)` |  |

### Table `program.kjks` <a id="table-program-kjks"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `kjks` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `skmenteri` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `chairmanname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `chairmanphonenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `secretaryname` | `character varying(50)` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 6 | `secretaryphonenumber` | `character varying(60)` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 7 | `treasurername` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `treasurerphonenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `photo1` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `photo2` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `photo3` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kjkstype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `spmaccount` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `spmdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `spmnumber` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `sp2daccount` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `sp2ddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `sp2dnumber` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.klaimtransaksiproject` <a id="table-program-klaimtransaksiproject"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `klaimtransaksiproject` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idtransaksiklaim` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idtransaksireferensi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nomorreferensi` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `totalnominal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `sisaklaim` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `tanggalbantuan` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tanggalklaim` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `sumberdana` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idtransaksiklaim)` |  |

### Table `program.konversiperolehanqurban` <a id="table-program-konversiperolehanqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `konversiperolehanqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `konversiperolehanqurbanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `rencanadistribusiid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `jumlahhewankonversi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nominalkonversi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `jenishewan` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (konversiperolehanqurbanid)` |  |

### Table `program.liabilityaccount` <a id="table-program-liabilityaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `liabilityaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `liabilityaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.liabilitytransactionitem` <a id="table-program-liabilitytransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `liabilitytransactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `liabilitytransactiontype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.linkedprograms` <a id="table-program-linkedprograms"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `linkedprograms` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `linkedprogramid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `linkedproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (linkedprogramid)` |  |

### Table `program.mapreconcile` <a id="table-program-mapreconcile"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mapreconcile` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
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

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mapid)` |  |

### Table `program.marginitem` <a id="table-program-marginitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `marginitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemstatementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cpp` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bmi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `bmm` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `microfin` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `development` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `profitsharing` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemstatementid)` |  |

### Table `program.marketingqurban` <a id="table-program-marketingqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `marketingqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `marketingqurbanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mqtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `bankaccountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branchcode` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (marketingqurbanid)` |  |

### Table `program.masjidkum3` <a id="table-program-masjidkum3"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `masjidkum3` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `afiliasiorganisasi` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `alamat` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `bendahara` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `contactperson` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `cpphone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `foto1` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `foto2` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `jumlahukm` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kecamatan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kegiatanmasjid` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kelurahan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `ketua` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `komunitasusahajamaah` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kota` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `mustahiqgroupid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 17 | `phonenumber` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 18 | `radiusukm` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `sekertaris` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `iseligible` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `noteligiblereason` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqgroupid)` |  |

### Table `program.masterjenisdonasiqurban` <a id="table-program-masterjenisdonasiqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `masterjenisdonasiqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `paketqurbanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `kodepaket` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `keteranganwilayah` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nominaldonasi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `feemarketer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `jenishewan` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (paketqurbanid)` |  |

### Table `program.mpz` <a id="table-program-mpz"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mpz` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `assets` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `candidatecount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 4 | `membercount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `unitsector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `zisfundpreviousmonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `zisfundthismonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `zisgrowthperyear` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.mpzzisallocation` <a id="table-program-mpzzisallocation"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mpzzisallocation` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `fundamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fundingperiodename` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `sectorname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `zisallocationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (zisallocationid)` |  |

### Table `program.mustahiq` <a id="table-program-mustahiq"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiq` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqreferenceby` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `program.mustahiqadditionalinfo` <a id="table-program-mustahiqadditionalinfo"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqadditionalinfo` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqinfoid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqinfotype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqidsupervisor` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `schoolname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `sd_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `sd_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `sd_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `smp_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `smp_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `smp_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `sma_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `sma_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `sma_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `achievement` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `universitas_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `universitas_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `universitas_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqinfoid)` |  |

### Table `program.mustahiqappraisal` <a id="table-program-mustahiqappraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqappraisal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (appraisalid)` |  |

### Table `program.mustahiqaqh` <a id="table-program-mustahiqaqh"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqaqh` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `depositbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `couplename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `couplejob` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `employeestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `position` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `program.mustahiqbankaccount` <a id="table-program-mustahiqbankaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqbankaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountusagetype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `statusaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `activedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nonactivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `bankstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `program.mustahiqcandidate` <a id="table-program-mustahiqcandidate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqcandidate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `boys` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 3 | `dependents` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `firstchildedu` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `girls` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `monthlyincome` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `secondchildedu` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `thirdchildedu` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `candidatestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `ethnicgroup` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `housingstatus` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `spousename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `verificator` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.mustahiqcorporate` <a id="table-program-mustahiqcorporate"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqcorporate` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `cpphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `cpmobilenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `program.mustahiqgroup` <a id="table-program-mustahiqgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqgroup` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqgroupid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `groupname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `islowlevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `detailid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `grouptype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `membercount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqgroupid)` |  |

### Table `program.mustahiqgroupdetail` <a id="table-program-mustahiqgroupdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqgroupdetail` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `detailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `detailname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `membercount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (detailid)` |  |

### Table `program.mustahiqkum3` <a id="table-program-mustahiqkum3"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqkum3` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `photo1` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `photo2` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `photo3` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `personalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `program.mustahiqliabilityaccount` <a id="table-program-mustahiqliabilityaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqliabilityaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mlatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.mustahiqpersonal` <a id="table-program-mustahiqpersonal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqpersonal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqgender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqbirthplace` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `mustahiqbirthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `mustahiqidentitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqreligion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqtotalfamily` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `mustahiqformaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqmarital` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `mustahiqworksector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mustahiqashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `mustahiqidentitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 13 | `programtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `mustahiqpersonaltype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `mustahiqtargetcapital` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `workid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `mustahiqincome` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `program.mustahiqproduct` <a id="table-program-mustahiqproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqproduct` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqextnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `iseligible` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `noteligiblereason` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqextfield` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `noteligibledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `noteligiblelegal` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastfundingperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `pendingfund` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `mustahiqproducttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `mustahiqproductid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 15 | `startdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `mustahiqproductname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `dateend` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `distributionamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `datestart` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `proposalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `mustahiqproductgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 23 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `fundproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `totalrecipient` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqproductid)` |  |

### Table `program.mustahiqproductgroup` <a id="table-program-mustahiqproductgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqproductgroup` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqproductgroupid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqproductgrouptype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqproductgroupname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqproductgroupid)` |  |

### Table `program.mustahiqproject` <a id="table-program-mustahiqproject"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqproject` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `detailklaimid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqproductid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqproductid)` |  |

### Table `program.mustahiqqurban` <a id="table-program-mustahiqqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `mustahiqqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqage` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `namalokasi` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `program.negara` <a id="table-program-negara"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `negara` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idnegara` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_negara` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idnegara)` |  |

### Table `program.orphanbalancepartition` <a id="table-program-orphanbalancepartition"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphanbalancepartition` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `balancepartitionid` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (balancepartitionid)` |  |

### Table `program.orphanbeasiswa` <a id="table-program-orphanbeasiswa"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphanbeasiswa` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `age` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `aschildnumber` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 4 | `dependent` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `fatheraddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `fatherbirthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `fatherbirthplace` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `fatherdeathdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `foundationname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `guardianincome` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `guarantor` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `housingstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `insurance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `insuranceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `isfatheralive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `ismotheralive` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 17 | `lifewith` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `monthlyelectricitycost` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `monthlycellularcost` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `monthlylandlinecost` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `monthlywatercost` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `motherbirthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 23 | `motherbirthplace` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 24 | `nickname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `onfoundation` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `onscholarship` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `scholarshipprovider` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `schooladdress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 29 | `schoolclass` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `schoolfees` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `schoolingstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `totaldebt` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `orphanksm` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.orphandebtlist` <a id="table-program-orphandebtlist"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphandebtlist` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `debtid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `category` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `loanvalues` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (debtid)` |  |

### Table `program.orphankafala` <a id="table-program-orphankafala"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphankafala` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `causeoforphanage` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `cpmobileno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 4 | `datekafalaended` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `datekafalastarted` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `extracircularactivities` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fathercauseofdeath` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fathercurrenteconomic` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `fathermarital` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `guardiancurrenteconomic` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `guardianphonenumber` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `hobbies` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `mentorremarks` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `mothercauseofdeath` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `mothercurrenteconomic` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 17 | `mothermarital` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 18 | `numberofbrothers` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `numberofsisters` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `olduisid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `piachangesstatus` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `registrationdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.orphankafalaliability` <a id="table-program-orphankafalaliability"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphankafalaliability` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.orphanksm` <a id="table-program-orphanksm"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphanksm` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `orphanlevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fotopeserta` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fotopenyakit` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `program.orphansiblings` <a id="table-program-orphansiblings"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphansiblings` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `siblingsid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `siblingsname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (siblingsid)` |  |

### Table `program.orphantertiarylist` <a id="table-program-orphantertiarylist"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `orphantertiarylist` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `tertiaryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `tertiaryname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `quantity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (tertiaryid)` |  |

### Table `program.parameterglobal` <a id="table-program-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `parameterglobal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_parameter)` |  |

### Table `program.parameterinbox` <a id="table-program-parameterinbox"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `parameterinbox` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kodeinbox` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `namaform` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `taginbox` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kodeinbox)` |  |

### Table `program.parameterjournal` <a id="table-program-parameterjournal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `parameterjournal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterjournalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `datasource` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `journalcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterjournalid)` |  |

### Table `program.parameterjournalitem` <a id="table-program-parameterjournalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `parameterjournalitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterjournalitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchbase` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `basesign` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currencybase` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `amountbase` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `ratebase` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountbase` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterjournalitemid)` |  |

### Table `program.partner` <a id="table-program-partner"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `partner` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `partnertype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `partnerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `partnercpname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `partnercpmobilephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `partnercpaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `partnercpemail` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `partnername` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (partnerid)` |  |

### Table `program.pequrban` <a id="table-program-pequrban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `pequrban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `referensi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `issudahprosesklaim` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `marketingqurbanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `atasnamarekening` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `nomorrekening` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `requestdistribusiid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid, productid)` |  |

### Table `program.perolehanqurban` <a id="table-program-perolehanqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `perolehanqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `perolehanqurbanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `jenisdonasi` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `ekuivalendana` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `claimtransactiondetailqurbanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `konversiperolehanqurbanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `paketqurbanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fotosebelum` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fotosetelah` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `fotosaat` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid, perolehanqurbanid)` |  |

### Table `program.picdistribusi` <a id="table-program-picdistribusi"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `picdistribusi` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `picdistribusiid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `bankaccountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (picdistribusiid)` |  |

### Table `program.product` <a id="table-program-product"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `product` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountofcollection` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountofdistribution` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `percentageofamilfunds` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `producttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `closeddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fixedvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `fixedvalueamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `parentproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `productcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `multipackage` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `nishab` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `haul` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `isquotafull` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `mustahiqquota` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `currentquotaposition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `productgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `transactionproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `program.productaccount` <a id="table-program-productaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `productaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.productdetail` <a id="table-program-productdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `productdetail` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productdetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `detailname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productdetailid)` |  |

### Table `program.productgroup` <a id="table-program-productgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `productgroup` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productgroupid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productgroupcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `statusaktif` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transactionproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productgroupid)` |  |

### Table `program.producthierarchy` <a id="table-program-producthierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `producthierarchy` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
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

### Table `program.producttarget` <a id="table-program-producttarget"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `producttarget` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `beginperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `endperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `producttargetid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (producttargetid)` |  |

### Table `program.producttargetcomponent` <a id="table-program-producttargetcomponent"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `producttargetcomponent` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `componentid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `producttargetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `targetcomponentname` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `targetfinalvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `targetunit` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `targetvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (componentid)` |  |

### Table `program.producttargethistory` <a id="table-program-producttargethistory"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `producttargethistory` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `componentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `currentvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `producttargethistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `updatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (producttargethistoryid)` |  |

### Table `program.producttransactionitem` <a id="table-program-producttransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `producttransactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `partitioncode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.program` <a id="table-program-program"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `program` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `programtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `program.programaqh` <a id="table-program-programaqh"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `programaqh` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  | UK | NO | none | reference_allowed | YES | needs_review |
| 3 | `maxplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `maxdropping` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |
| `programaqh_branchcode_key` | UNIQUE | `UNIQUE (branchcode)` |  |

### Table `program.programksm` <a id="table-program-programksm"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `programksm` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `programterkaitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `program.programqurban` <a id="table-program-programqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `programqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `yearimplementation` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `hijriyahyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `totaldonation` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `program.project` <a id="table-program-project"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `project` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `budgetamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `startdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `finsihdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `program.projectaccount` <a id="table-program-projectaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `projectaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `startdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `finishdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `budgetamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.propinsi` <a id="table-program-propinsi"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `propinsi` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idpropinsi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `propinsi` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kodepropinsi` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idpropinsi)` |  |

### Table `program.proposal` <a id="table-program-proposal"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `proposal` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `proposalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `proposaldate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `proposaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `proposalno` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `proposalnominal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `proposalreceivedby` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `proposalreceiveddate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `proposalreferenceby` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `proposalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `proposalreferenceposition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `productgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (proposalid)` |  |

### Table `program.realisasidistribusi` <a id="table-program-realisasidistribusi"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realisasidistribusi` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realisasidistribusiid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `rencanadistribusiid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `jumlahhewanqurban` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `fotolokasi` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `bentukdistribusi` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `alasanperubahan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realisasidistribusiid)` |  |

### Table `program.realisasidistribusihewan` <a id="table-program-realisasidistribusihewan"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realisasidistribusihewan` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realisasidistribusihewanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `rencanadistribusihewanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `jumlah` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `realisasidistribusiid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `jenishewan` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realisasidistribusihewanid)` |  |

### Table `program.realization` <a id="table-program-realization"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realization` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realizationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realizationdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realmemoid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `realizationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `realizationdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `realizationinputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `realizationinputuser` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `realizationlocation` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `memoamount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `budgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `realizationamount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `partnerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `statusreceivables` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `statusreclpj` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realizationid)` |  |

### Table `program.realizationbudget` <a id="table-program-realizationbudget"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationbudget` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realbudgetid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `budgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realbudgetid)` |  |

### Table `program.realizationcost` <a id="table-program-realizationcost"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationcost` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realizationcostid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `costitemid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `costamount` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `realizationcosttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `returnid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realizationcostid)` |  |

### Table `program.realizationdetail` <a id="table-program-realizationdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationdetail` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realizationdetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realizationamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `memoamount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `realizationdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `detaildescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `cashaacountno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `fundproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realizationdetailid)` |  |

### Table `program.realizationmemo` <a id="table-program-realizationmemo"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationmemo` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realmemoid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realmemonumber` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realmemosubject` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `realmemoamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `realmemofrom` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `realmemoto` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `realizationmemotype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `userinput` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `realmemodate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `dokumenid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realmemoid)` |  |

### Table `program.realizationmemodetail` <a id="table-program-realizationmemodetail"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationmemodetail` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realmemodetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realmemodetailamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realmemoid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realmemodetailid)` |  |

### Table `program.realizationpartner` <a id="table-program-realizationpartner"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationpartner` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realizationpartnerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `partnerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (realizationpartnerid)` |  |

### Table `program.realizationphoto` <a id="table-program-realizationphoto"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationphoto` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `photoid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `photofilename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `photodescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (photoid)` |  |

### Table `program.realizationreturn` <a id="table-program-realizationreturn"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationreturn` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `returnid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `returndate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `returndescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `returnamount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputuser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `authuser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `authdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `costamount` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (returnid)` |  |

### Table `program.realizationreturndetail` <a id="table-program-realizationreturndetail"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationreturndetail` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `returndetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `returnamount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `detaildescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `realizationamount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `returnid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `realizationdetailid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (returndetailid)` |  |

### Table `program.realizationtransactionitem` <a id="table-program-realizationtransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `realizationtransactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `transactionproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `budgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `fundproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `partnerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `returnamount` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `distributionamount` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `statusrecrepdetailid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.reconcileprocess` <a id="table-program-reconcileprocess"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `reconcileprocess` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `reconcileprocessid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reconciledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `reconcileuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `reconcileterminal` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `processstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `statementmonth` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `statementyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `isallstatementproceed` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `numberofproceed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `reconciletype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (reconcileprocessid)` |  |

### Table `program.reconciletransaction` <a id="table-program-reconciletransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `reconciletransaction` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `banktransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reconciledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `userreconcile` | `character varying(80)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `klaim` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `saldo` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `accountdebet` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (banktransactionid)` |  |

### Table `program.reconciletransactionqurban` <a id="table-program-reconciletransactionqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `reconciletransactionqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `reconciletransactionqurbanid` | `integer CONSTRAINT reconciletransactionqurban_reconciletransactionqurbani_not_null` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `banktransactionid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `reconciledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userreconcile` | `character varying(80)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountdebet` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (reconciletransactionqurbanid)` |  |

### Table `program.region` <a id="table-program-region"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `region` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `regionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `regionname` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (regionid)` |  |

### Table `program.rekeningpenghimpunanqurban` <a id="table-program-rekeningpenghimpunanqurban"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `rekeningpenghimpunanqurban` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rekeningpenghimpunanqurbanid` | `integer CONSTRAINT rekeningpenghimpunanqurban_rekeningpenghimpunanqurbani_not_null` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `active` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nomorrekening` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rekeningpenghimpunanqurbanid)` |  |

### Table `program.rencanadistribusi` <a id="table-program-rencanadistribusi"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `rencanadistribusi` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rencanadistribusiid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `namalokasi` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `bentukdistribusi` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `jumlahhewanqurban` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nominaldana` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `keterangan` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rencanadistribusiid)` |  |

### Table `program.rencanadistribusihewan` <a id="table-program-rencanadistribusihewan"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `rencanadistribusihewan` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rencanadistribusihewanid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `ekuivalendana` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `rencanajumlah` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jenishewan` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `rencanadistribusiid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rencanadistribusihewanid)` |  |

### Table `program.requestdistribusi` <a id="table-program-requestdistribusi"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `requestdistribusi` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `requestdistribusiid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `namalokasi` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (requestdistribusiid)` |  |

### Table `program.reversetransaction` <a id="table-program-reversetransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `reversetransaction` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
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

### Table `program.sessionblob` <a id="table-program-sessionblob"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `sessionblob` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sessionid` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sessioncontext` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `program.statusreceivablereport` <a id="table-program-statusreceivablereport"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `statusreceivablereport` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `statusreceivableid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `programtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `realmemoid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `receivablereportamount` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `receivablereportdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `receivableinputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `receivablereportdesc` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `receivablereportstatus` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `receivablereportuserauth` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `receivablereportuserinput` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `lastupdatedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `lastupdateuser` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (statusreceivableid)` |  |

### Table `program.statusrecrepdetail` <a id="table-program-statusrecrepdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `statusrecrepdetail` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `statusrecrepdetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `detaildescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `realizationamount` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `reportamount` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `statusreceivableid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `realizationdetailid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `reportdetailstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `recipientname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `recipientphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `processdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `updatedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `updateuser` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (statusrecrepdetailid)` |  |

### Table `program.tmp_budget` <a id="table-program-tmp-budget"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `tmp_budget` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `budgetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `program.tmp_migmustahiqproduct` <a id="table-program-tmp-migmustahiqproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `tmp_migmustahiqproduct` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqextnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `iseligible` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `noteligiblereason` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqextfield` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `noteligibledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `noteligiblelegal` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastfundingperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `pendingfund` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `mustahiqproducttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `startdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `mustahiqproductname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `dateend` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `distributionamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `datestart` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `proposalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `mustahiqproductgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 23 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `ashnaf` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `fundproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `program.tmp_migrasikodepos` <a id="table-program-tmp-migrasikodepos"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `tmp_migrasikodepos` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `baris` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `kode_pos` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `desa` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `is_valid` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_auth` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kecamatan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kode_kecamatan` | `character varying(7)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kota` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `kode_kota` | `character varying(7)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `propinsi` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kode_propinsi` | `character varying(7)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `program.transaction` <a id="table-program-transaction"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `transaction` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputer` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `authuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transactiontime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `isposted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `transactionblockid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `channelcode` | `character varying` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `paidto` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `receivedfrom` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 22 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `isauthorized` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `coretransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `coretransactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `transactiontype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `realizationid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `returnid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `statusreceivableid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `coresourcetransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `sourcetransactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `program.transactionaccount` <a id="table-program-transactionaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `transactionaccount` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `linkaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `opendate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `usercreated` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `userotorized` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `datecreated` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `dateotorized` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `terminalcreated` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `terminalotorized` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `transactionaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `currency_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `branchcode` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.transactionitem` <a id="table-program-transactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `transactionitem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currencycode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `refaccountname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `paidto` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `isinternalpaidto` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.transactiontype` <a id="table-program-transactiontype"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `transactiontype` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactioncode` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `vouchercode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactioncode)` |  |

### Table `program.uploadedstatement` <a id="table-program-uploadedstatement"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `uploadedstatement` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `uploadedstatementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reconcileprocessid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `uploaddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userfilename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `systemfilename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `isuploadsucceed` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isreconciled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `reconcileuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `statementyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `statementmonth` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `ispicapprove` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `isbasereconciled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `ismarginreconciled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (uploadedstatementid)` |  |

### Table `program.visit` <a id="table-program-visit"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `visit` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `visitid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `visitdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `visitlocation` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `visitbegintime` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `visitendtime` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `visitaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `visittype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (visitid)` |  |

### Table `program.visititem` <a id="table-program-visititem"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `visititem` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `visititemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `visititemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `visititemannotation` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `visitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (visititemid)` |  |

### Table `program.visitperson` <a id="table-program-visitperson"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `visitperson` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `visitpersonid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `visitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `visitpersonname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `visitpersonposition` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `visitpersontype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (visitpersonid)` |  |

### Table `program.volunteer` <a id="table-program-volunteer"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `volunteer` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `volunteerid` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `volunteername` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `homeaddress` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `homephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `mobilephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `email` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `totalamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (volunteerid)` |  |

### Table `program.volunteertransaction` <a id="table-program-volunteertransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `volunteertransaction` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `volunteerid` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `program.vproduct` <a id="table-program-vproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `vproduct` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `productname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 4 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `producttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `currencycode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `percentageofamilfunds` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `idx` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `program.worksector` <a id="table-program-worksector"></a>

| Field | Value |
| --- | --- |
| Schema | `program` |
| Table | `worksector` |
| Domain | `Needs Review` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `statusaktif` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workid)` |  |
