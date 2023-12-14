const Sidebar = () => {
    return (
      <div className="sidebar bg-white text-white p-4 flex flex-col rounded-md shadow-md">
        {/* Seu conteúdo do menu lateral aqui */}
        <button className="bg-blue-500 text-black p-2 rounded-full shadow-md mb-4">
          Autos de Infração
        </button>
        <button className="bg-green-500 text-black p-2 rounded-full shadow-md mb-4">
          Importar autos de infração
        </button>
        <button className="bg-red-500 text-black p-2 rounded-full shadow-md">
          Gerar recurso
        </button>
      </div>
    );
  };

export default Sidebar;