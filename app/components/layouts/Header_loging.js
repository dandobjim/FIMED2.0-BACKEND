import React from 'react';
import Nav_loging from './Nav_loging';
import Link from 'next/link';

const Header_loging = () => {
    return ( 
        <header>
            <div>
                <div>
                    <p>Logo</p>
                    <Nav_loging/>
                </div>

                <div>
                    <Link href = '/docs'>Documentation</Link>
                </div>

            </div>
        </header>
     );
}
 
export default Header_loging;