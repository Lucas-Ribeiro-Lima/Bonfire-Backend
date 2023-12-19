import MainApp from "@/components/mainApp"
import ImportForm from "@/components/import/importForm"
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
