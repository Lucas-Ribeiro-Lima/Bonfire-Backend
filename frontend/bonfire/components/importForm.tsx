// 'use client';

import React, {useState, useEffect} from "react";
// import GetAutoInfracaoPrimeiraInstancia from "../services/apiClient";

const ImportForm = () => {
    // const [data, setData] = useState(null);

    // useEffect(() => {
    //   const fetchData = async () => {
    //     try {
    //       const response = await GetAutoInfracaoPrimeiraInstancia();
    //       setData(response);
    //       console.log(response);
    //     } catch (error) {
    //       console.error("Erro ao obter dados:", error);
    //     }
    //   };
  
    //   fetchData();
    // }, []); 
    
    return (
        <form className="flex flex-col gap-4" encType="multipart/form-data">
            <label className="flex flex-col gap-4">
                Selecione o arquivo:
                <input type='file' className='rounded-lg'></input>
            </label>
            <div className="flex flex-row gap-4">
                <label className='flex gap-2'>
                <input type='checkbox' name='Instancia' value='1Instancia'></input>
                1° Instância
                </label>
                <label className="flex gap-2">
                <input type='checkbox' name='Instancia' value='2Instancia'></input>
                2° Instância
                </label>
            </div>
            <button type='submit' className="bg-zinc-200/50 w-max rounded-lg text-black p-1 hover:bg-white hover:duration-500">Importar</button>
        </form>
    );
}

export default ImportForm