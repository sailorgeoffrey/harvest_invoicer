# Invoice

**Date:** {{invoice.date}}

**Geoffrey Chandler**  
U Havlíčkových sadů 1422/15  
120 00 Prague 2 - Vinohrady  
Czech Republic

*geoffrey.chandler@aboutobjects.com*  
+420 755 075 035

**Robert E Leonard, CEO**  
**About Objects**  
11911 Freedom Drive, Suite 700  
Reston, VA 20190  
United States of America  
+1 (571) 346-7544

|                    |                        |
|--------------------|------------------------|
| **Start Date:**    | {{invoice.start_date}} |
| **End Date:**      | {{invoice.end_date}}   |
| **Hourly Rate:**   | {{invoice.rate}}       |
| **Payment Terms:** | {{invoice.terms}}      |
| **Due Date:**      | {{invoice.due}}        |


| Client | Hours | Description | Item Total |
|:-------|:------|-------------|-----------:|
{% for item in items %}
| {{item.client}} | {{item.hours}} | {{item.description}} | {{item.total}} |
{% endfor %}
| | |           **Total:** | {{invoice.total}} |
