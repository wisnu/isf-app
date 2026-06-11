# Skill: nuwis-skill-daf-reader
## Panduan Membaca Kode Legacy DAF (Python 2/Jython)

Gunakan skill ini ketika membaca file-file di `docs/legacy-apps/` untuk analisis
migrasi. Skill ini menjelaskan struktur DAF, pattern yang perlu dikenali, dan cara
mengekstrak business logic yang tersembunyi.

---

## Struktur DAF

```
docs/legacy-apps/{modul}/
├── dialogs/
│   └── {Domain}/
│       └── {fFormName}/
│           ├── _intr.py         ← client-side event handlers
│           ├── _data.py         ← server-side: load + save logic
│           ├── {fFormName}.svr  ← field definitions
│           └── {fFormName}.dfr  ← visual layout
├── menus/
│   ├── {nama}.mnu               ← menu tree + permissions
│   └── {nama}.py                ← event handlers (app.CreateForm)
├── scripts/
│   └── {X}/
│       └── {Y}.py               ← backend script entry points
├── script_modules/
│   └── {ClassName}.py           ← shared business logic classes
└── default.mcf                  ← class registry + lib registry
```

---

## Membaca File `.mnu`

Format XML-like proprietari DAF:

```
object:rmn::MenuItem<
  Caption='Kas Masuk'
  OnClick='FundCollectionClick'
  AllowedGroups='KEU;ACC;SPVKEU'
  StringTag='Transaksi/fFundCollection'
>
```

**Cara parse**:
- `Caption` → label menu UI
- `AllowedGroups` → pisah `;` → list role code
- `StringTag` format `{Domain}/{fFormName}` → path dialog: `dialogs/{Domain}/{fFormName}/`
- `OnClick='ShowQueryClick'` → langsung ke dialog dari StringTag
- `OnClick` lainnya → baca `menus/{nama}.py`, cari `app.CreateForm(path, ...)`

**Pola app.CreateForm:**
```python
def FundCollectionClick(self, *args):
    app.CreateForm('Transaksi/fFundCollection', mode='new')
```
→ path dialog: `dialogs/Transaksi/fFundCollection/`

---

## Membaca File `.svr` (Field Definitions)

```
object:frm::FieldDef<
  FieldName='TransactionDate'
  DataType='Date'
  Required='True'
  Caption='Tanggal Transaksi'
>
```

**Extract**: FieldName, DataType, Required (True/False/blank=False), Caption

DataType mapping:
- `Date` → `DateField.vue` + Python `date`
- `Currency` → number Input + `Decimal`
- `String` → text Input + `str`
- `Integer` → number Input + `int`
- `Boolean` → Checkbox + `bool`

---

## Membaca File `.dfr` (Visual Layout)

```
object:frm::Section<
  SectionName='Detail'
  fields={
    object:frm::FieldRef< FieldName='Amount' ReadOnly='True' >
    object:frm::FieldRef< FieldName='Notes' Visible='False' >
  }
>
```

**Extract**:
- `SectionName` → nama tab/section di Vue form
- `ReadOnly='True'` → field auto-filled, bukan user input
- `Visible='False'` → field tersembunyi tapi disimpan ke DB (discriminator atau sistem)

---

## Membaca `_intr.py` (Client-Side Logic)

File ini adalah "event handler" UI. Pattern yang penting:

```python
# ExecuteScript = endpoint API baru di isf-app
self.ExecuteScript('Transaksi.GetDonorList', {'search': self.txtDonor.Value})
# → endpoint GET /api/transaksi/donor-list

# Validasi sebelum save
def ValidateForm(self):
    if not self.txtAmount.Value:
        raise ValidationError("Jumlah harus diisi")

# CallServerMethod = trigger save
self.CallServerMethod('SimpanData', {'mode': 'new'})
```

**Setiap `ExecuteScript('X.Y', ...)` = satu API endpoint baru di isf-app.**

---

## Membaca `_data.py` (Server-Side Logic)

File ini punya dua fungsi utama:

```python
# FormSetDataEx = load default values (→ onMounted di Vue)
def FormSetDataEx(self, form, params):
    form.TglTransaksi.Value = config.Now()  # default tanggal hari ini
    form.CabangId.Value = config.SecurityContext.BranchId  # dari session
    # Load dropdown list
    form.DonorList.Value = self.GetDonorList()

# SimpanData = save (→ service.py di api-python)
def SimpanData(self, form, params):
    config.BeginTransaction()
    try:
        obj = helper.CreatePObject('FundTransaction')  # → lookup di default.mcf
        obj.TransactionDate = form.TglTransaksi.Value
        obj.Amount = form.Amount.Value
        obj.Save()
        obj.CreateJournal()  # → jurnal akuntansi
        config.Commit()
    except:
        config.Rollback()
        raise
```

**FormSetDataEx → pre-fills untuk `onMounted()` di Vue.**
**SimpanData → business logic untuk `service.create_xxx()` di api-python.**

---

## Trace `CreatePObject` (Object Registry)

`helper.CreatePObject('FundTransaction')` → lookup di `default.mcf`:

```ini
[classlist]
FundTransaction = fundtransaction

[liblist]
fundtransaction = FundTransactionModule.py
```

→ buka `script_modules/FundTransactionModule.py`:
```python
class FundTransaction(BaseObject):
    def Save(self):
        # INSERT ke tabel FUND_TRANSACTION
        self.config.Execute("INSERT INTO FUND_TRANSACTION (...) VALUES (...)")
    
    def CreateJournal(self):
        # INSERT ke tabel JOURNAL_ENTRY
```

**Catat**: tabel DB yang di-INSERT, kolom yang di-set, FK relationships.

---

## Pattern Python 2 yang Sering Muncul

```python
# Exception syntax Python 2
raise Exception, 'message'  # → raise Exception('message')

# Dict check
if dict.has_key('key'):     # → if 'key' in dict:

# JSON (inhouse library)
import simplejson
data = simplejson.loads(srequest)  # → json.loads()

# String formatting
print "Hello %s" % name  # → f-string atau format()

# Integer division (Python 2 default)
a = 5 / 2  # = 2  ← Python 2 integer division!

# Old-style class
class MyClass:  # tidak extends object

# Tuple unpacking in except
except Exception, e:  # → except Exception as e:
```

---

## Discriminator Patterns yang Sering Ditemukan

Discriminator tersembunyi sering ada di `SimpanData` atau `CreatePObject`:

```python
# Explicit discriminator
obj.AccountType = 'D'  # → accounttitype = 'D' (Penghimpunan)
obj.AccountType = 'Z'  # → accounttitype = 'Z' (Penyaluran)

# Dari parameter form
obj.ARType = params.get('ar_type', 'E')  # E=Karyawan, D=Non-Karyawan, C=Rekap

# Dari kode akun
obj.KodeAkun = '530000'  # Amil
```

**Temukan discriminator ini di `_data.py` atau `script_modules/` dan catat di MIGRATION_ANALYSIS.**
