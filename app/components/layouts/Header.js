import React from 'react';
import Nav from './Nav';
import Link from 'next/link';
import styled from '@emotion/styled';
import {css} from '@emotion/core';


const ContenedorHeader = styled.div`
    max-width: 1200px;
    width: 95%;
    margin: 0 auto;
    @media (min-width:768px){
        display: flex;
        justify-content: space-between;
    }
    background-color: #FFF;
    
`;

const Logo = styled.img`
    background-color:#FFF;
    margin-left: 1rem;
    margin-right: 2rem;
`;

const Header = () => {
    return ( 
        <>
            <header
                css = {css`
                    border-bottom: 2px solid #e1e1e1;
                    padding:  0;
                `}
            >
                <ContenedorHeader>
                    <div>
                        <div>
                            <Link href="/">
                            <Logo className="logo" src="/static/img/Fimed_logo.png" />
                            </Link>
                            
                        </div>
                        

                        <Nav/>
                    </div>
                    <div>
                        <p> Hola: Usuario</p>

                        <button type ="button">Cerrar Sesion</button>
                    </div>
                </ContenedorHeader>
            </header>
        </>
     );
}
 
export default Header;
