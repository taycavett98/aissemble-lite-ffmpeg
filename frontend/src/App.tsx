/*
 * Copyright 2025 Booz Allen Hamilton.
 *
 * Booz Allen Hamilton Confidential Information.
 *
 * The contents of this file are the intellectual property of
 * Booz Allen Hamilton, Inc. ("BAH") and are subject to copyright protection
 * under the laws of the United States and other countries.
 *
 * You acknowledge that misappropriation, misuse, or redistribution of content
 * on the file could cause irreparable harm to BAH and/or to third parties.
 *
 * You may not copy, reproduce, distribute, publish, display, execute, modify,
 * create derivative works of, transmit, sell or offer for resale, or in any way
 * exploit any part of this code or program without BAH's express written permission.
 *
 * The contents of this code or program contains code
 * that is itself or was created using artificial intelligence.
 *
 * To the best of our knowledge, this code does not infringe third-party intellectual
 * property rights, contain errors, inaccuracies, bias, or security concerns.
 *
 * However, Booz Allen does not warrant, claim, or provide any implied
 * or express warranty for the aforementioned, nor of merchantability
 * or fitness for purpose.
 *
 * Booz Allen expressly limits liability, whether by contract, tort or in equity
 * for any damage or harm caused by use of this artificial intelligence code or program.
 *
 * Booz Allen is providing this code or program "as is" with the understanding
 * that any separately negotiated standards of performance for said code
 * or program will be met for the duration of any applicable contract under which
 * the code or program is provided.
 */

import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
