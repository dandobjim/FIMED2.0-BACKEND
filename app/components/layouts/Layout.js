import React from 'react';
import {Global, css} from '@emotion/core';
import Header from './Header'
import Head from 'next/head';

const Layout = props => {
    return ( 
        <>  
            <Global 
                styles ={css`
                    html {
                        position: relative;
                        min-height: 100%;
                    }
                    body {
                        background: #93939c;
                        /*min-width: 768px;*/
                        padding-top: 70px;
                        font-family: 'PT Sans', sans-serif;
                    }
                    h1, h2, h3, h4, a {
                        color: #e26d17;
                    }

                    h1, h2, h3, h4 {
                        font-family: "Roboto Slab", serif;

                    }

                    h2 {
                        font-size: 24px;
                    }
                    h3 {
                        font-size: 18px;
                    }
                    h4 {
                        font-size: 14px;
                        font-weight: 700;
                    }

                    element.style {
                        width: 246px;
                    }

                    .btn-space {
                        margin-right: 5px;
                    }

                    input[type=text], .txtarea{
                        /*text-transform: capitalize;*/
                        margin-bottom: 10px;

                    }
                    a:hover, a:focus {
                        color: #C4551C;
                    }
                    thead {
                        background-color: rgba(235, 105, 9, 0.65);
                        /*color: white;*/
                    }
                    .table-hover>tbody>tr:hover {
                        background-color: #DEDEDE;
                    }

                    .logo-container {
                        background: white;
                        padding: 5px 0px;
                    }
                    .ecompass-logo {
                        margin: 10px;
                    }
                    .khaos-logo {
                        margin-top: 6px;
                        margin-bottom: 3px;
                    }
                    .black-bar {
                        background: #222;
                        height: 40px;
                        margin-bottom: 20px;
                        padding: 9px;
                        color :#EEE;
                    }
                    .starter-template {
                    padding: 40px 15px;
                    text-align: center;
                    }
                    .footer {
                        text-align: center;
                        /* position: absolute; */
                        /* bottom: 0; */
                        width: 100%;
                        /* height: 40px; */
                        /* background-color: #f5f5f5; */
                    }
                    .panel-ecompass-footer {
                        background-color: #222;
                        border-color: #222;
                    }
                    .panel-ecompass-footer > .panel-body {
                        padding: 0px;
                        color: #EEE;
                    }
                    .footer-container {
                        margin: 10px;
                    }
                    .navbar-collapse {
                        padding-left: 15px !important;
                        padding-right: 15px !important;
                    }
                    .btn-default {
                        color: #EB6909;
                        background-color: #fff;
                        border-color: #EB6909;
                    }
                    .btn-default:active, .btn-default:hover,
                    .btn-default:focus,
                    .btn-default.active.focus, .btn-default.active:focus,
                    .btn-default.active:hover, .btn-default:active.focus,
                    .btn-default:active:focus, .btn-default:active:hover,
                    .open>.dropdown-toggle.btn-default.focus,
                    .open>.dropdown-toggle.btn-default:focus,
                    .open>.dropdown-toggle.btn-default:hover {
                        background-color: white;
                        background-color: #e6e6e6;
                        color: #EB6909;
                        border-color: #EB6909;
                    }
                    .btn-primary {
                        color: #fff;
                        background-color: #EB6909;
                        border-color: #AD430C;
                    }
                    .btn-primary:active, .btn-primary:hover,
                    .btn-primary:focus,
                    .btn-primary.active.focus, .btn-primary.active:focus,
                    .btn-primary.active:hover, .btn-primary:active.focus,
                    .btn-primary:active:focus, .btn-primary:active:hover,
                    .open>.dropdown-toggle.btn-primary.focus,
                    .open>.dropdown-toggle.btn-primary:focus,
                    .open>.dropdown-toggle.btn-primary:hover {
                        color: #fff;
                        background-color: #C4551C;
                        border-color: #AD430C;
                    }
                    .btn-primary.disabled.focus, .btn-primary.disabled:focus,
                    .btn-primary.disabled:hover, .btn-primary[disabled].focus,
                    .btn-primary[disabled]:focus, .btn-primary[disabled]:hover,
                    fieldset[disabled] .btn-primary.focus, fieldset[disabled] .btn-primary:focus,
                    fieldset[disabled] .btn-primary:hover {
                        background-color: #C4551C;
                        border-color: #AD430C;
                    }
                    .btn-link {
                        font-weight: bold;
                        font-weight: 800;
                        color: #eba203;
                    }
                    .btn-link:focus, .btn-link:hover {
                        color: #eb6909;
                    }
                    .btn-default.active, .btn-default:active, .open>.dropdown-toggle.btn-default {
                        border-color: #EB6909;
                        color: #fff;
                        background-color: #C4551C;
                    }
                    .btn-group>.btn:not(:first-child):not(:last-child):not(.dropdown-toggle) {
                        border-radius: 3px;
                    }
                    .btn-group-label {
                        padding-top: 6px;
                        font-size: 12px;
                        padding-right: 15px;
                        padding-left: 15px;
                        font-weight: 700;
                        display: inline-block;
                    }

                    .btn-block {
                        display: block;
                        width: 100%;
                    }
                    .dropdown-menu>.active>a, .dropdown-menu>.active>a:focus, .dropdown-menu>.active>a:hover {
                        background-color: #EB6909;
                    }
                    .progress-bar {
                        background-color: #EB6909;
                    }
                    .popover-title {
                        background-color: #EB6909;
                        color: white;
                    }
                    .popover-content {
                        color: rgb(51,51,51);
                    }
                    .slider-handle {
                        background-color: #EB6909 !important;
                        background-image: -webkit-linear-gradient(top, #eb6909 0,#C4551C 100%);
                        background-image: -o-linear-gradient(top,#EB6909 0,#C4551C 100%);
                        background-image: linear-gradient(to bottom,#EB6909 0,#C4551C 100%);
                        background-repeat: repeat-x;
                    }
                    @media (max-width: 768px) {
                        img.logo {
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                        float: none !important;
                        }
                    }
                    .result-help-btn {
                        font-weight: 800;
                        width: 22px;
                        height: 22px;
                    }
                    [ng\:cloak], [ng-cloak], [data-ng-cloak], [x-ng-cloak], .ng-cloak, .x-ng-cloak {
                    display: none !important;
                    }

                    /* /* MELANOMA STYLE */
                    .form-inline > .form-group > select {
                        margin-right: 20px;
                        margin-left: 5px;
                    }
                    .melanoma-well {
                        padding: 10px;
                    }
                    .melanoma-ol {
                        padding-left: 30px;
                        margin-bottom: 0px;
                    }

                    .melanoma-python-img {
                        max-width: 100%;
                    }

                    .slider-container {
                        margin-top: 7px;
                    }


                    .center-block {
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }


                    LOADER

                    .alert-melanoma {
                        color: #58585a;
                        background-color: whitesmoke;
                        border-color: #58585a;
                    }

                    .loader {
                        border: 6px solid #58585a;
                        border-top: 6px solid #EB6909;
                        border-radius: 50%;
                        width: 20px;
                        height: 20px;
                        animation: spin 2s linear infinite;
                    }

                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }

                    .slidecontainer {
                        width: 100%; /* Width of the outside container */
                    }

                    /* The slider itself */
                    .slider {
                        -webkit-appearance: none;  /* Override default CSS styles */
                        appearance: none;
                        width: 100%; /* Full-width */
                        height: 10px; /* Specified height */
                        background: #d3d3d3; /* Grey background */
                        outline: none; /* Remove outline */
                        opacity: 0.7; /* Set transparency (for mouse-over effects on hover) */
                        -webkit-transition: .2s; /* 0.2 seconds transition on hover */
                        transition: opacity .2s;
                    }

                    /* Mouse-over effects */
                    .slider:hover {
                        opacity: 1; /* Fully shown on mouse-over */
                    }

                    /* The slider handle (use -webkit- (Chrome, Opera, Safari, Edge) and -moz- (Firefox) to override default look) */
                    .slider::-webkit-slider-thumb {
                        -webkit-appearance: none; /* Override default look */
                        appearance: none;
                        width: 10px; /* Set a specific slider handle width */
                        height: 10px; /* Slider handle height */
                        background: #eb6909; /* Green background */
                        cursor: pointer; /* Cursor on hover */
                    }

                    .slider::-moz-range-thumb {
                        width: 10px; /* Set a specific slider handle width */
                        height: 10px; /* Slider handle height */
                        background: #eb6909; /* Green background */
                        cursor: pointer; /* Cursor on hover */
                    }



                    /* Center the loader */
                    #loader {
                        position: absolute;
                        left: 50%;
                        z-index: 1;
                        width: 100px;
                        height: 100px;
                        margin: -100px 0 0 -75px;
                        border: 16px solid #f3f3f3;
                        border-radius: 50%;
                        border-top: 16px solid #eb6909;
                        -webkit-animation: spin 2s linear infinite;
                        animation: spin 2s linear infinite;
                    }

                    @-webkit-keyframes spin {
                        0% { -webkit-transform: rotate(0deg); }
                        100% { -webkit-transform: rotate(360deg); }
                    }

                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }

                    /* Add animation to "page content" */
                    .animate-bottom {
                        position: relative;
                        -webkit-animation-name: animatebottom;
                        -webkit-animation-duration: 1s;
                        animation-name: animatebottom;
                        animation-duration: 1s
                    }

                    @-webkit-keyframes animatebottom {
                        from { bottom:-100px; opacity:0 }
                        to { bottom:0px; opacity:1 }
                    }

                    @keyframes animatebottom {
                        from{ bottom:-100px; opacity:0 }
                        to{ bottom:0; opacity:1 }
                    }

                    label{
                        margin-bottom: 10px;
                    }

                    .form-control{
                        margin: 2px;
                    }

                    .button-field{
                        margin-top: 20px;
                        margin-bottom: 20px;
                        width: 179px;
                    }

                    .table{
                        font-size: 12px;
                    }
                `}
            />

            <Head>
                <html lang='es' />
                <title>FIMED</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css" 
                integrity="sha256-WAgYcAck1C1/zEl5sBl5cfyhxtLgKGdpI3oKyJffVRI=" 
                crossorigin="anonymous" />
                <link href="https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&family=Roboto:wght@400;700&display=swap" 
                rel="stylesheet"/>
            </Head>

            <Header />
            
            
            
            <main>
                {props.children}
            </main>
        </>
     );
}
 

export default Layout;