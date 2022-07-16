# Bring in the Cavalry

## Where it All Started
* The given `.zip` file contains 2 files (within a `stage_0` folder):
  * ![](2022-07-16-19-11-41.png)
* Opening the `key.txt` file gives us:
  * ![](2022-07-16-19-13-52.png)
* Since the top of the file says `PNG`, I changed the file extension to `.png` and openning it as a png gives us the key - `N0_Brutef0rce`:
  * ![](key.png)
* The other file provided (`Trusted_Relationships.png`) is an encrypted pdf which requires a password to be accessed:
  * ![](2022-07-16-19-16-47.png)
* Entering the key from before (`N0_Brutef0rce`) gives us access to the pdf
  * ![](2022-07-16-19-19-07.png)
* I tried looking reading the document, clicking on some of the links and checking the documents metadata, all to no avail
* Finally found it after converting the `.pdf` into a `.txt` and *Ctrl+F*ing the document:
  * ![](2022-07-16-19-28-11.png)
* `CTF{Th1rd_P@rty_Vend0r5_@re_R15ky}`

