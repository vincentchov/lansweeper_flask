S E L E C T 
    h t b l t i c k e t . t i c k e t i d   a s   T i c k e t I D ,
     h t b l t i c k e t t y p e s . t y p e n a m e   a s   T i c k e t T y p e , 
    t b l a s s e t s . A s s e t N a m e   a s   A s s e t N a m e,
     t s y s A s s e t T y p e s . A s s e t T y p e n a m e   a s   A s s e t T y p e N a m e  ,
     h t b l c u s t o m f i e l d s . f i e l d i d   a s   F i e l d I D  ,
     h t b l c u s t o m f i e l d s . n a m e   a s   F i e l d N a m e  ,
     h t b l t i c k e t c u s t o m f i e l d . d a t a   a s   F i e l d D a t a 
  F R O M   [ l a n s w e e p e r d b ] . [ d b o ] . [ h t b l t i c k e t ] 
      / *   F i e l d D a t a   * / 
I N N E R   J O I N   h t b l t i c k e t c u s t o m f i e l d   
       O N   h t b l t i c k e t . t i c k e t i d   =   h t b l t i c k e t c u s t o m f i e l d . t i c k e t i d 
    / *   F i e l d N a m e   * / 
  I N N E R   J O I N   h t b l c u s t o m f i e l d s 
     O N   h t b l t i c k e t c u s t o m f i e l d . f i e l d i d   =   h t b l c u s t o m f i e l d s . f i e l d i d 
    / *   A s s e t N a m e   * / 
  I N N E R   J O I N   t b l a s s e t s 
       O N   h t b l t i c k e t . a s s e t i d   =   t b l a s s e t s . a s s e t i d 
    / *   A s s e t T y p e N a m e   * / 
I N N E R   J O I N   t s y s A s s e t T y p e s 
    O N   t b l a s s e t s . A s s e t T y p e   =   t s y s A s s e t T y p e s . A s s e t T y p e 
      / *   T i c k e t T y p e   * / 
  I N N E R   J O I N   h t b l t i c k e t t y p e s 
       O N   h t b l t i c k e t . t i c k e t t y p e i d   =   h t b l t i c k e t t y p e s . t i c k e t t y p e i d 
W H E R E   h t b l t i c k e t t y p e s . t y p e n a m e   L I K E   ' I T   S u p p o r t ' ; 
