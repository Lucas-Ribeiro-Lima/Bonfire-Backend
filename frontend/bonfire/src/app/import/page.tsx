import MainApp from "@/components/mainApp"
import Layout from "@/components/primaryLayout"
<<<<<<< HEAD
import ImportForm from "@/components/importForm"
=======
import ImportForm from "@/components/import/importForm"
>>>>>>> 5a095e2717059e60de386bb706c2c6d50fa357d8
import PrimaryLayout from "@/components/primaryLayout"

export default function Home() {
  return (
      <PrimaryLayout>
        <MainApp title="Importação de Autos de Infração">
          <ImportForm></ImportForm>
        </MainApp>
      </PrimaryLayout>
    )
}
