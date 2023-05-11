defmodule Bananas do
  defp to_integer([num, string]) do
    [:erlang.binary_to_integer(num), string]
  end

  defp to_integer(list) do
    list
  end

  defp print_flag(false) do
    IO.puts("Nope")
  end

  defp print_flag(true) do
    IO.puts(File.read!("flag.txt"))
  end

  def main(args) do
    print_flag(check(convert_input(IO.gets("How many bananas do I have?\n"))))
  end

  def main() do
    super([])
  end

  defp convert_input(string) do
    to_integer(String.split(String.trim(string)))
  end

  defp check([num, "bananas"]) do
    :erlang.==(:erlang.-(:erlang.*(:erlang.+(num, 5), 9), 1), 971)
  end

  defp check(_asdf) do
    false
  end
end