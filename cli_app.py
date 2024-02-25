from pathlib import Path
import click
from mrpsolver import Part, Solver


def draw_bom(part: Part, solver: Solver, level: int=0) -> None:
    """ Prints a visual tree representing the indented BOM of a part """
    for ch, qt in part.bom.items():
        child = solver.all_parts[ch]
        click.echo(' '+level*'|  '+'|- '+ child.id +'   (qt: '+str(qt)+')')
        draw_bom(child, solver, level +1)

def header_rows(solver: Solver) -> str:
    top_row = '{:10s}'.format('Part')+''.join('{:^8d}'.format(e) for e in range(solver.min_period, solver.max_period+1))
    line_row = (10 + 8 * (solver.max_period - solver.min_period + 1)) * '-'
    return top_row, line_row

def available_table(available: dict):
    for part_id, quantities in available.items():
        click.echo('{:10s}'.format(part_id)+''.join('{:^8}'.format(e) for e in quantities))

def mrp_table(mrp: dict):
    for part_id, quantities in mrp.items():
        click.echo('{:10s}'.format(part_id)+''.join('{:^8}'.format(e) for e in quantities))

@click.command(help="Calculate an MRP order-release schedule from provided IMF, MPS, and BOM files.")
@click.option(
    "-i",
    "--imf",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "-m",
    "--mps",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "-b",
    "--bom",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "--show_bom", 
    is_flag=True,
)
def cli(imf, mps, bom, show_bom):
    """ """
    solver = Solver()

    click.echo("Loading Item Master File...")
    solver.load_imf(imf)
    click.echo("Item Master File successfully loaded.")

    click.echo("Loading Master Production Schedule...")
    solver.load_mps(mps, "part")
    click.echo("Master Production Schedule successfully loaded.")

    click.echo("Loading Bill of Materials...")
    solver.load_bom(bom)
    click.echo("Bill of Materials successfully loaded.")

    click.echo("Solving...")
    mrp, available = solver.solve()
    click.echo("Solved!")
    
    click.echo(' Result '.center(100, '-')+'\n\n')
    if show_bom:
        click.echo('-  Indented BOM  -'+'\n')
        for part in solver.orphans:
            click.echo(" "+part.id)
            draw_bom(part, solver)
            click.echo('')

    top_row, line_row = header_rows(solver)

    click.echo('\n\n'+"-  Available To Promise Quantities Per Time Period  -"+'\n')
    click.echo(top_row)
    click.echo(line_row)
    available_table(available)

    click.echo('\n\n'+"-  MRP Order-Release Schedule  -"+'\n')
    click.echo(top_row)
    click.echo(line_row)
    mrp_table(mrp)


if __name__ == "__main__":
    cli()