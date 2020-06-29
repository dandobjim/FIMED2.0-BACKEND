import React from 'react';
import Link from 'next/link';

const Nav = () => {
    return ( 
        <nav>
            <Link href="/">Home</Link>
            <Link href="/pacientes">Patients</Link>
            <Link href="/analysis">Analysis</Link>
        </nav>
     );
}
 
export default Nav;