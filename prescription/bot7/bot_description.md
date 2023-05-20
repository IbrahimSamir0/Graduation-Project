<!-- ```mermaid
classDiagram
      Animal <|-- Duck
      Animal <|-- Fish
      Animal <|-- Zebra
      Animal : +int age
      Animal : +String gender
      Animal: +isMammal()
      Animal: +mate()
      class Duck{
          +String beakColor
          +swim()
          +quack()
      }
      class Fish{
          -int sizeInFeet
          -canEat()
      }
      class Zebra{
          +bool is_wild
          +run()
      }
``` -->
class diagrame
---
---

```mermaid

classDiagram

    PARENT<|-- INTERACTION
    PARENT<|-- SIDEEFFECTS
    PARENT<|-- DRUG
    INTERACTION<|--RUN
    SIDEEFFECTS<|--RUN
    DRUG<|--RUN


    class PARENT{
        ~instance 
        ~wait
        ~open()
        +landFirstPage()
        +search()
        +back()
        +closePopUp()
        +closeSmallPopUp()
        +hashing(txt)
    }
    
    class INTERACTION{
        +click_interaction() ---->click interaction link
        +get_interaction_drugs() ------> click links block
        +get_name_of_active_ingredient()
        -getIntSource(clas)
        -getIntText(clas)
        -getIntLinks(clas)
        -validDescription(txt)
        -getInteractionDescription()
        -active_ingredient() ingredient
        +getDrugInteraction(drug_name)
        
    }

    class SIDEEFFECTS{
        -side_effects : map
        +clickFirstLink()
        +clickSideEffectLink(drug_name)
        +get_side_effects()
        +run_add_side_effects_db()
    }

    class DRUG{
        +parent : PARENT Instance
        +con : DB Instance
        +driver : WEBDRIVER
        +drug : String
        +description : DESCRIPTION Instance
        +interaction : INTERACTION Instance
        +drugs_names : List

        +split_name_from_active_ingredient()
        +get_name_and_active_ingredient()
        +is_ingredient_has_None()
        +is_ingredient_has_0()
        +is_ingredient_has_1()
        _add_drug_ingredient_to_db()
        _add_ingredient_and_interactions()
        _add_drug_description()
        +add_drug_to_db()
    }

    class RUN{
        -get_active_ingredient_for_user_drug()
        +prepare_drugs()
    }
```

-------
Flow chart
---
---

```mermaid
graph TD
A[Hard edge] -->B(Round edge)
    B --> C{get Drug }
    C -->|One| D[from website in constant file]
    C -->|Two| E[drugs from user]
    D --> F{is active ingredient in db?}
    F --> |Yes| f[Save drug]
    f --> |No| G[get ingredient interaction with other ingredients ]
    G -->g[Save drug]
```


