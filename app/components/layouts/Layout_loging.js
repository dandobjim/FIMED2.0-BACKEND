import React from 'react';
import Link from 'next/link';
import Header_loging from './Header_loging';


const Layout_loging = props => {
    return ( 
        <>
            
            <Header_loging/>
            
            <main>
                {props.children}
            </main>
        </>
     );
}
 

export default Layout_loging;