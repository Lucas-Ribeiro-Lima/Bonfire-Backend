import MainApp from "@/components/mainApp"
import Layout from "@/components/primaryLayout"
import ImportForm from "@/components/importForm"

export default function Home() {
  return (
      <Layout>
        <MainApp title="Importação de Autos de Infração">
          <ImportForm></ImportForm>
        </MainApp>
      </Layout>
    )
}
