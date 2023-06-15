<h1 align="center">DME Configurator</h1>
<p align="center">An application to add or remove DM Extensions for Honeywell DMCs.</p>

<p align="center">
    <img src="images\interface_DME.png" alt="Empty interface">
</p>

## Installation

1. Copy the "DMRL Editor_V2.zip" to a convenient location on your PC.
2. Extract the contents at same location.
3. Cut and paste "catalog" folder directly in C: or replace if any old "catalog" folder exists.
4. Now inside "DMRL Editor" in local folder copy "main.exe" and do "paste as shortcut" outside "DMRL Editor" folder.
5. Double click the shortcut to launch the application.

<p align="center">
    <img src="images\install.png" alt="Installation">
</p>

## Getting Started

### Prerequisites

#### catalog

> To support each sub applications of DMRL editor, the "catalog" directory should be present in the local drive "C:" directly.

## Usage and description

### Usage

1. The application includes 8 sub processes namely,`<br>`
   i.   Refreshing DMCs `<br>`
   ii.  Brex validation `<br>`
   iii.  Replacing idents `<br>`
   iv.  Validation of cross references `<br>`
   v.   Creating DMRL `<br>`
   vi.  Verifying DMRL `<br>`
   vii.  Applying DMRL `<br>`
   viii. Generation of empty data modules `<br>`
2. Authors can use the processes as per their convenience in authoring process.
3. Before applying DMRL, the "cross reference validation" and DMRL verification has to be done manditorily.
4. The application only supports to edit ATA specific DMCs. No generic modules will be edited including local or common repositories.

### Description

1. Refreshing DMCs:

   - Helps to rename DMCs inside as named outside.
   - Updates character entities and graphical entites.
   - Updates DOCTYPE definition of each DMC.
   - Creates a text log report in the working folder named as "dmc-refresh.log"
2. Validate Brex:

   - Validates number of brex included in "C:\catalog\Brex" against the working folder.
   - Creates a docx log report in the working folder named as, "brex-validation.docx".
3. Implement Auto-idents:

   - Changes or updates the idents given to the particulars as per CSDB requirement.
   - Updates "irtt" for each idents given.
   - Creates a text log report in the working folder named as "id-replacement.log"
4. Validate cross references:

   - Validates cross references and referred fragments if present in each DMC.
   - Creates a docx report in the working folder named as "cross_ref-validation.docx".
5. Create/Rewrite DMRL:

   - Creates DMRL based on the attributes given in each DMC. Otherwise rewrites the existing DMRL.
   - Creates a text log report named as "dmrl-creation.log" in the working folder.
6. Verify DMRL:

   - Verifies modified DMRL agaist three factors.

     i. File existance check:

     - Checks each file listed in first column of DMRL i.e., "filename" whether it is present in the working folder or not.

     ii. Pattern match:

     - Verifies each attributes given in the DMRL against a set of Reguler expressions alloted, and reports back if it dosn't match.

     iii. Value and duplecate DMC check:

     - Checks for the allowable infocode values.
     - Checks for the duplicate resulting DMCs.
   - creates a text log report as "dmrl-verification.log" inside working folder.
7. Apply DMRL:

   - Modifies the DMCs as per attributes given in DMRL.
   - Updates DMC references within PMC.
   - If one choose to change "Descriptive" schema to "Procedural" or vice versa, the schema will be changed accordingly and each elements will be updated.
   - The Apply DMRL
8. Generate empty data modules:

   - Genertes empty DMCs by looking at the PMC.
   - The empty DMC will be created only if it dosn't exist in the folder.

> NOTE:
>
> 1. Kindly perform "cross reference verification" and "DMRL verification" processes before applying the DMRL.
> 2. Keep a backup copy of the working folder before performing any atomization process.
> 3. The application is only compatible for S1000D 4-1 issue.

### Summary

#### Description of functions

| Function                    | Description                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| Create/Rewrite DMRL         | Creates DMRL based on the attributes given in each DMC present.                  |
| Verify DMRL                 | Verifies the DMRL whether it is applicable or not.                               |
| Apply DMRL                  | Modifies DMCs as per changes made in DMRL.                                       |
| Generate Empty Data Modules | Generate empty DMCs if it dosn't exist in the directory.                         |
| Refresh DMCs                | Refreshes DMC for character entities, graphic entities and Inner dmCode address. |
| Validate Brex               | Validates number of brex included against the document                           |
| Implement Auto-idents       | Changes idents given for each particular as per CSDB requirement                 |
| Validate Cross References   | Validates cross references given among the DMCs.                                 |

#### Ident name and patterns

| Ident name        | IRTT   | Pattern                                     | Example                      |
| ----------------- | ------ | ------------------------------------------- | ---------------------------- |
| Figure            | irtt01 | fig-[0-9]{4}                                | fig-1234                     |
| Table             | irtt02 | tab-[0-9]{4}                                | tab-1234                     |
| Supply            | irtt04 | sup-[0-9]{4,5}                              | sup-1234 or sup-12345        |
| Support Equipment | irtt05 | seq-[0-9]{4,5}                              | seq-1234 or seq-12345        |
| Spare             | irtt06 | spa-[0-9]{4}                                | spa-1234                     |
| Levelled para     | irtt07 | par-[0-9]{4}                                | par-1234                     |
| Step              | irtt08 | stp-[0-9]{4}                                | stp-1234                     |
| Graphic           | irtt09 | gra-[0-9]{4}                                | gra-1234                     |
| Multimedia Object | irtt10 | mmo-[0-9]{4}                                | mmo-1234                     |
| Hotspot           | irtt11 | (fig-[0-9]{4}-gra-[0-9]{4}-AUTOID_[0-9]{3}) | fig-1234-gra-1234-AUTOID_123 |
| Para              | irtt51 | para-[0-9]{4}                               | par-1234                     |

#### Schema configuration of S1000D_4-1

| Schema Type         | Schema Name            | Schema Value                                                                                                                        |
| ------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| brex                | Brex 4.1               | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/brex.xsd'>`brex `</a>`                                               |
| crew                | Crew 4.1               | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/crew.xsd'>`crew `</a>`                                               |
| appliccrossreftable | ACT 4.1                | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/appliccrossreftable.xsd'>`applicability cross reference table `</a>` |
| checklist           | Checklist 4.1          | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/checklist.xsd'>`checklist `</a>`                                     |
| comrep              | CIR 4.1                | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/comrep.xsd'>`common repository `</a>`                                |
| container           | Container 4.1          | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/container.xsd'>`container `</a>`                                     |
| condcrossreftable   | CCT 4.1                | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/condcrossreftable.xsd'>`conditional cross reference table `</a>`     |
| descript            | Descriptive 4.1        | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/descript.xsd'>`descriptive `</a>`                                    |
| fault               | Fault 4.1              | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/fault.xsd'>`fault `</a>`                                             |
| frontmatter         | Front Matter 4.1       | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/frontmatter.xsd'>`front matter `</a>`                                |
| learning            | Learning 4.1           | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/learning.xsd'>`learning `</a>`                                       |
| ipd                 | IPD 4.1                | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/ipd.xsd'>`illustrated parts data `</a>`                              |
| proced              | Procedural 4.1         | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/proced.xsd'>`procedural `</a>`                                       |
| process             | Process 4.1            | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/process.xsd'>`process `</a>`                                         |
| prdcrossreftable    | PCT 4.1                | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/prdcrossreftable.xsd'>`product cross reference table `</a>`          |
| pm                  | Publication Module 4.1 | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/pm.xsd'>`publication module `</a>`                                   |
| schedul             | Schedule 4.1           | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/schedul.xsd'>`schedule `</a>`                                        |
| wrngdata            | Wiring Data 4.1        | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/wrngdata.xsd'>`wiring data `</a>`                                    |
| wrngflds            | Wiring Fields 4.1      | `<a href='http://www.s1000d.org/S1000D_4-1/xml_schema_flat/wrngflds.xsd'>`wiring fields `</a>`                                  |

## Testing

1. The tested and verified documents are listed below.`<br>`
   i. `<a href='file:///F:/CMM/2. Support/1. Honeywell/10. Tool/13. DMRL_Editor/Testing/S1000D-D200509000034R006'>`49-25-87 `</a><br>`
   ii. `<a href='file:///F:\CMM\2. Support\1. Honeywell\10. Tool\13. DMRL_Editor\Testing\DMRL_09072022_CMM'>`27-08-01 `</a><br>`
   iii. `<a href='file:///F:\CMM\2. Support\1. Honeywell\10. Tool\13. DMRL_Editor\Testing\DMRL_09072022_EMM'>`72-04-07 `</a><br>`

## Updates

1. The application is now compatible to change DMC from descriptive to procedural schema or vice versa.
2. The application is now can able to define DOCTYPE automatically.
